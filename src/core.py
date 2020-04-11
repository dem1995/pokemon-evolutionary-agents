import enum
import typing
import functools
import inspect
import uuid
import random

import anytree
from poke_env.environment.pokemon_type import PokemonType
from poke_env.environment.weather import Weather
from poke_env.player.player import Player
from poke_env.environment.battle import Battle
from .DSL import DSL, StatValue, TypeMultiplier, MovePower, OptionalWeather

RULE: typing.Optional[enum.Enum] = None
GRAMMAR: typing.Optional[enum.Enum] = None


def get_node_id():
    return str(uuid.uuid4())[:8]


class Node(anytree.Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._id = get_node_id()

    def __eq__(self, other):
        return anytree.RenderTree(self).by_attr() == anytree.RenderTree(other).by_attr()

    def __hash__(self):
        return str(anytree.RenderTree(self).by_attr()).__hash__()

    def print(self, ascii_=False, call_log=False):
        def _format_node(node):
            return str(node.name) + (' (X) ' if node.id_ in call_log else '')

        style = anytree.render.AsciiStyle() if ascii_ else anytree.render.ContStyle()

        if not call_log:
            print(anytree.RenderTree(self, style=style).by_attr())
        else:
            print(anytree.RenderTree(self, style=style).by_attr(_format_node))


class Script(object):
    def __init__(self, tree, raw_script):
        super().__init__()
        self.tree = tree
        self.raw_script = raw_script


DEFAULT_RULES = [
    "START",
    "IF_BLOCK",
    "IF_BODY",
    "BOOL_EXP",
    "AND_EXP",
    "NOT_EXP",
    "OR_EXP",
    "BOOL",
    "CHANGE_SCORE",
    "SCORE_NUM",
    "PLUS_EQ_OR_MINUS_EQ",
    "RETURN",
    "LIB_CALL",
    # "FLOAT_NUM",
    # "INT_NUM",
    "TYPE_MULTIPLIER_FLOAT_NUM",
    "STAT_VALUE_INT_NUM",
    "MOVE_POWER_INT_NUM",
    "NUM_COMPARATOR",
    "ENUM_COMPARATOR",
    "POKEMON_TYPE",
    "OPTIONAL_WEATHER",
]


def log_call(func):
    @functools.wraps(func)
    def _wrapper(*args):
        self, id_, *rest = args
        self.call_log.add(id_)
        return func(*rest)

    return _wrapper


def make_dynamic_rule(name, func):
    param_lookup = {
        'self': 'self',
        'move': 'move',
        # 'float_num': RULE.FLOAT_NUM,
        # 'int_num': RULE.INT_NUM,
    }
    if name != '__init__':
        params = list(map(param_lookup.get, inspect.signature(func).parameters))[1:]
        return_type = typing.get_type_hints(func).get('return', None)
        func_name = 'dsl.' + name.lower()
        # if return_type is int:
        #     rule = [func_name, *params, RULE.NUM_COMPARATOR, RULE.INT_NUM]
        # elif return_type is float:
        #     rule = [func_name, *params, RULE.NUM_COMPARATOR, RULE.FLOAT_NUM]
        if return_type is TypeMultiplier:
            rule = [func_name, *params, RULE.NUM_COMPARATOR, RULE.TYPE_MULTIPLIER_FLOAT_NUM]
        elif return_type is StatValue:
            rule = [func_name, *params, RULE.NUM_COMPARATOR, RULE.STAT_VALUE_INT_NUM]
        elif return_type is MovePower:
            rule = [func_name, *params, RULE.NUM_COMPARATOR, RULE.MOVE_POWER_INT_NUM]
        elif return_type is PokemonType:
            rule = [func_name, *params, RULE.ENUM_COMPARATOR, RULE.POKEMON_TYPE]
        elif return_type is OptionalWeather:
            rule = [func_name, *params, RULE.ENUM_COMPARATOR, RULE.OPTIONAL_WEATHER]
        elif return_type is bool:
            rule = [func_name, *params]
        else:
            print(f"{func_name} return type hint not valid.")
            return None
        return rule


class Sampler(object):
    def sample(self):
        raise NotImplementedError


class Diminishing(Sampler):
    def __init__(self, gamma, rule):
        self.gamma = gamma
        self.rule = rule

    def sample(self):
        ret = []
        curr = 1
        while random.random() <= curr:
            ret.append(self.rule)
            curr *= self.gamma
        return ret


class Weighted(Sampler):
    def __init__(self, dict_):
        self.dict = dict_

    def sample(self):
        weight_sum = sum(self.dict.keys())
        normal_coefficient = 1 / weight_sum
        rand = random.random()
        for weight, rule in self.dict.items():
            prob = weight * normal_coefficient
            if rand <= prob:
                if not isinstance(rule, list):
                    rule = [rule]
                return rule
            else:
                rand -= prob
        raise ValueError


def init():
    global RULE, GRAMMAR

    lib_functions = inspect.getmembers(DSL, inspect.isfunction)

    RULE = enum.Enum('Rule', DEFAULT_RULES + [name.upper() for name, _ in lib_functions])

    dynamic_rules = [make_dynamic_rule(name, func) for name, func in lib_functions]
    print(dynamic_rules)
    dynamic_rules = [rule for rule in dynamic_rules if rule]

    GRAMMAR = {
        RULE.START: [
            Diminishing(0.7, RULE.IF_BLOCK),
        ],
        RULE.IF_BLOCK: [
            [RULE.BOOL_EXP, RULE.IF_BODY],
        ],
        RULE.IF_BODY: [
            RULE.CHANGE_SCORE
        ],
        RULE.BOOL_EXP: [
            RULE.BOOL,
            RULE.AND_EXP,
            RULE.NOT_EXP,
        ],
        RULE.AND_EXP: [
            [RULE.BOOL, RULE.BOOL],
        ],
        RULE.NOT_EXP: [
            RULE.BOOL,
        ],
        RULE.OR_EXP: [
            [RULE.BOOL, RULE.BOOL],
        ],
        RULE.BOOL: [
            RULE.LIB_CALL,
        ],
        RULE.CHANGE_SCORE: [
            RULE.SCORE_NUM
        ],
        RULE.SCORE_NUM: [str(num) for num in range(-8, 9) if num != 0],
        # RULE.FLOAT_NUM: [str(2 ** num) for num in range(-2, 3)],
        # RULE.INT_NUM: [str(num) for num in range(256)],
        RULE.TYPE_MULTIPLIER_FLOAT_NUM: [str(num) for num in TypeMultiplier.okay_values],
        RULE.STAT_VALUE_INT_NUM: [str(num) for num in StatValue.okay_values],
        RULE.MOVE_POWER_INT_NUM: [str(num) for num in MovePower.okay_values],
        RULE.POKEMON_TYPE: ['PokemonType.' + t.name for t in PokemonType],
        RULE.OPTIONAL_WEATHER: ['Weather.' + w.name for w in Weather] + ['None'],
        RULE.NUM_COMPARATOR: [
            "<=", ">="
        ],
        RULE.ENUM_COMPARATOR: [
            "==", "!="
        ],

        RULE.LIB_CALL: dynamic_rules,
    }


def generate_tree(root):
    if isinstance(root.name, str):
        return root
    next_ = GRAMMAR.get(root.name, None)
    if not next_:
        raise ValueError

    branch = random.choice(next_)

    candidates = []
    if isinstance(branch, list):
        candidates = branch
    elif isinstance(branch, (RULE, str)):
        candidates = [branch]
    elif isinstance(branch, Sampler):
        candidates.extend(branch.sample())
    elif branch is None:
        pass
    else:
        raise ValueError

    for candidate in candidates:
        child = Node(candidate, parent=root)
        generate_tree(child)
    return root


def get_random_tree(seed=None):
    if seed:
        random.seed(seed)
    root = Node(RULE.START)
    tree = generate_tree(root)

    return tree


def indent(raw, level):
    tab = '    '
    lines = raw.splitlines()
    lines = [tab * level + line for line in lines]
    return '\n'.join(lines)


script_template = r"""
class {0}(Script):
    def choose_move(self, battle: Battle):
    
        available_moves = battle.available_moves
        if not available_moves:
            return self.choose_random_move(battle)
            
        dsl = DSL(battle)
        move_scores = []
        for move in battle.available_moves:
            score = 0
{1}
            move_scores.append(score)
            
        best_move = available_moves[move_scores.index(max(move_scores))]
        return best_move
"""


def derive(node):
    if isinstance(node.name, str):
        return node.name
    elif isinstance(node.name, RULE):
        if node.name == RULE.IF_BLOCK:
            template = "if ({0}):\n{1}\n"
            bool_exp = derive(node.children[0])
            body = indent(derive(node.children[1]), 1)
            return template.format(bool_exp, body)
        elif node.name == RULE.AND_EXP:
            template = "({0} and {1})"
            left = derive(node.children[0])
            right = derive(node.children[1])
            return template.format(left, right)
        elif node.name == RULE.OR_EXP:
            template = "({0} or {1})"
            left = derive(node.children[0])
            right = derive(node.children[1])
            return template.format(left, right)
        elif node.name == RULE.NOT_EXP:
            template = "not ({0})"
            op = derive(node.children[0])
            return template.format(op)
        elif node.name == RULE.CHANGE_SCORE:
            template = "score += {0}"
            delta = derive(node.children[0])
            return template.format(delta)
        elif node.name == RULE.LIB_CALL:
            if (
                len(node.children) >= 2
                and
                node.children[-2].name in (RULE.NUM_COMPARATOR, RULE.ENUM_COMPARATOR)
            ):
                # func call with a comparision expression
                template = "({0}({1}) {2} {3})"
                func_name, *args, comparator, rhs = node.children
                func_name = derive(func_name)
                params = ', '.join(derive(arg) for arg in args)
                comparator = derive(comparator)
                rhs = derive(rhs)
                return template.format(func_name, params, comparator, rhs)
            else:
                template = "{0}({1})"
                func_name, *args = node.children
                func_name = derive(func_name)
                params = ', '.join(derive(arg) for arg in args)
                return template.format(func_name, params)
        return ''.join(derive(child) for child in node.children)


def render_script(node):
    script_name = 'Script_' + str(uuid.uuid4()).replace('-', '')
    code = indent(derive(node), 3)
    return script_name, script_template.format(script_name, code)


def exec_tree(root):
    raw_script_class, raw_script = render_script(root)
    try:
        exec(raw_script)
        script_class = eval(raw_script_class)
        return script_class(root, raw_script)
    except Exception as e:
        print(e)
        print(raw_script)


def main():
    print(GRAMMAR)
    for i in range(20):
        get_random_tree(seed=i).print()


init()

if __name__ == '__main__':
    main()
