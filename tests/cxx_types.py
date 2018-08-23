
from capdpa.CXX import *

number = Namespace("Number",
        None,
        [Class(Identifier(["Number"]),
            Function("", "", [Variable(Identifier(["value"]), Type(Identifier(["int"]), 4, True))], Type(Identifier(["Number"]), 8, False)),
            [Variable(Identifier(["_value"]), Type(Identifier(["int"]), 4, True))],
            [Function(Identifier(["abs"]), "", [Variable(Identifier(["value"]), Type(Identifier(["int"]), 4, True))], Type(Identifier(["int"]), 4, True))],
            )],
        [Constant(Identifier(["ONE"]), 1), Constant(Identifier(["TWO"]), 2)],
        [Enum("NEGATIVE", [Constant(Identifier(["ONE"]), -1), Constant(Identifier(["TWO"]), -2)])])
