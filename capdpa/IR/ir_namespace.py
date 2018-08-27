import ir
import ir_class

class Namespace(ir_class.Class):

    def __init__(self, name, namespaces=None, classes=None, constants=None, enums=None):
        self.namespaces = namespaces or []
        self.classes = classes or []
        self.constants = constants or []
        self.enums = enums or []
        super(Namespace, self).__init__(name      = name,
                                        constants = constants,
                                        enums     = enums)
        self.constructors = None

    def __repr__(self):
        return "Namespace(name={}, namespaces={}, classes={}, constants={}, enums={})".format(
                self.name, self.namespaces, self.classes, self.constants, self.enums)
