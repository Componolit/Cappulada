
import unittest
from capdpa import *

class Capdpa_Test(unittest.TestCase):


    check = lambda self, a, b: self.assertEqual(a, b, "Invalid entity: >>>\n" + str(a) + "\n<<< expected: >>>\n" + str(b) + "\n<<<")
    load = lambda self, spec: open("tests/data/" + spec, "r").read()
    cache = lambda self, res, spec: open("tests/cache/" + spec, "w").write(res)

    def check_integration(self, header, specs):
        result = []
        ada_spec = lambda ir: result.extend(ir.AdaSpecification()) if\
                type(ir.AdaSpecification()) == type([]) else\
                result.append(ir.AdaSpecification())
#        print(CXX("tests/data/" + header).ToIR()[0].AdaSpecification())
        map(ada_spec, CXX("tests/data/" + header).ToIR())
        self.assertEqual(len(specs), len(result), "Expected {} compilation units, got {}\n====\n{}"
                .format(len(specs), len(result), result))
        map(self.cache, result, specs)
        map(self.check, result, map(self.load, specs))

