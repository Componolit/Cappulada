import ir
import ir_type
import ir_identifier
import ir_function
import ir_variable
import ir_class
import ir_namespace
import ir_constant
import ir_enum

class Class_Reference(ir.Base):

    def __init__(self, name):
        self.name = name

    def getClass(self):
        return self.GetRoot()[self.name.PackageFull()[1:]]

    def isVirtual(self):
        return self.getClass().isVirtual()

    def IsPrivate(self):
        return False

    def InstantiateTemplates(self):
        pass

    def UsedTypes(self, parent):
        if parent == self.name.PackageFull()[:-1]:
            return []
        return [self.name.PackageFull()]

    def AdaSpecification(self, indentation=0, private=False):
        converted = map(self.ConvertName, self.name.PackageFull())
        name = converted[-1]
        return " " * indentation + name + " : " + ".".join(converted + ['Class'])

    def PackagePath(self):
        return self.name.PackageFull()

class Unit(ir.Base):

    def UsedPackages(self):
        packages = map(lambda x: x, self.UsedTypes(self.FullyQualifiedName()))
        return sorted(list(set([".".join (map(self.ConvertName, p)) for p in packages])))
