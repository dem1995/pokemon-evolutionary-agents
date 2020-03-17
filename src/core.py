import enum
import typing
import functools
import inspect
import uuid
import random

import anytree

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
    def __init__(self, tree):
        super().__init__()
        self.tree = tree

    def get_action(self):
        raise NotImplementedError


DEFAULT_RULES = [
    "START",
    "IF_BLOCK",
    "IF_BODY",
    "BOOL_EXP",
    "AND_EXP",
    "NOT_EXP",
    "BOOL",
    "RETURN",
    "LIB_CALL",
]


def log_call(func):
    @functools.wraps(func)
    def _wrapper(*args):
        self, id_, *rest = args
        self.call_log.add(id_)
        return func(*rest)

    return _wrapper


class Lib(object):
    @log_call
    def get_teammates():
        return []

    @log_call
    def get_opponents():
        return []

    @log_call
    def get_active_pokemon():
        return []

    @log_call
    def get_active_opponent():
        return []


class DSL(object):
    pass


def make_dynamic_rule(name, func):
    params = list(inspect.signature(func).parameters)

    def _convert(param):
        if param == 'self':
            return 'self'
        else:
            raise ValueError

    return ['Lib.' + name.lower(), *list(map(_convert, params))]


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
    lib_functions = inspect.getmembers(Lib, inspect.isfunction)
    # lib_func_names = [
    #     name.upper()
    #     for name, _ in lib_functions if name[0] != '_'
    # ]

    RULE = enum.Enum('Rule', DEFAULT_RULES + [name.upper() for name, _ in lib_functions])

    dynamic_rules = [make_dynamic_rule(name, func) for name, func in lib_functions]

    GRAMMAR = {
        RULE.START: [
            RULE.IF_BLOCK,
        ],
        RULE.IF_BLOCK: (
            [RULE.BOOL_EXP, RULE.IF_BODY],
        ),
        RULE.IF_BODY: [
            RULE.RETURN,
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
        RULE.BOOL: [
            RULE.LIB_CALL,
        ],
        RULE.LIB_CALL: dynamic_rules,
    }


def generate_tree(root):
    if isinstance(root.name, str):
        return root
    next_ = GRAMMAR.get(root.name, None)
    if not next_:
        return root

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
        child = Node(candidate, parent=root, id_=get_node_id())
        generate_tree(child)
    return root


def get_random_tree(seed=None):
    if seed:
        random.seed(seed)
    root = Node(RULE.START, id_=get_node_id())
    tree = generate_tree(root)
    return tree


def main():
    init()
    print(GRAMMAR)
    for i in range(10):
        get_random_tree(seed=i).print()


if __name__ == '__main__':
    main()

# class MyScript(Script):
#     def get_action(self, state):
#         actions = state.available_moves()
#         scores = []
#         for a in actions:
#             score = 0
#
#             # generated code
#             if Lib.get_active_opponent():
#                 score += 1
#
#             if not Lib.get_active_opponent():
#                 score -= 2
#             # generated code
#
#             scores.append(score)
#         return actions[scores.index(max(scores))]
