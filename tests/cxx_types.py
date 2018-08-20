
from capdpa.CXX import *

number = Namespace("Number",
        None,
        [Class("Number",
            Function("", "", [Variable("value", Type("int", 4, True))], Type("Number", 8, False)),
            [Variable("_value", Type("int", 4, True))],
            [Function("abs", "", [Variable("value", Type("int", 4, True))], Type("int", 4, True))],
            )],
        [Constant("ONE", 1), Constant("TWO", 2)],
        [Enum("NEGATIVE", [Constant("ONE", -1), Constant("TWO", -2)])])
