import inspect
import uuid

import anytree


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
    "FUNC_CALL",
    "COLUMN_NUM",
    "SMALL_NUM",
]


class Lib(object):
    @classmethod
    def


class DSL(object):
    pass


lib_functions = inspect.getmembers(Lib, inspect.isfunction)

Rule
grammar = {
    Rule.START: [
        Rule.IF_BLOCK,
    ],
    Rule.IF_BLOCK: (
        [Rule.BOOL_EXP, Rule.IF_BODY],
    ),
    Rule.IF_BODY: [
        Rule.RETURN,
    ],
    Rule.BOOL_EXP: [
        #         Rule.BOOL_EXP,
        Rule.BOOL,
        Rule.AND_EXP,
        Rule.NOT_EXP,
    ],
    Rule.AND_EXP: [
        #         Weighted({
        #             7: [Rule.BOOL, Rule.BOOL],
        #             3: [Rule.BOOL_EXP, Rule.BOOL_EXP]
        #         })
        [Rule.BOOL, Rule.BOOL],
    ],
    Rule.NOT_EXP: [
        Rule.BOOL,
    ],
    Rule.BOOL: (
        Rule.FUNC_CALL,
    ),
    Rule.FUNC_CALL: [
        make_dynamic_rule(name) for name in lib_func_names
    ],
    Rule.RETURN: (
        "return a",
    ),
    Rule.COLUMN_NUM: [
        '2', '3', '4', '5', '6'
    ],
    Rule.SMALL_NUM: (
        '0', '1', '2', '3'
    )
}
grammar
