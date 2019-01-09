import ir
import ir_type
import ir_identifier
import ir_function
import ir_variable

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

    def AdaSpecification(self, indentation=0, private=False):
        converted = map(self.ConvertName, self.name.PackageFull())
        name = converted[-1]
        return " " * indentation + name + " : " + ".".join(converted + ['Class'])

    def PackagePath(self):
        return self.name.PackageFull()

class Unit(ir.Base):

    def UsedPackages(self):
        types = []

        def isLocalType(t):
            return self.FullyQualifiedName()[:len(t.PackagePath())] != t.PackagePath() and \
                   t.PackagePath()[:len(self.FullyQualifiedName())] != self.FullyQualifiedName()

        for f in filter(ir_function.Function.isInst, self.children):
            map(lambda p: types.append(p.ctype), f.parameters)
            if f.return_type:
                types.append(f.return_type)

        map(lambda v: types.append(v.ctype), filter(ir_variable.Member.isInst, self.children))
        map(lambda t: types.append(t.reference), filter(lambda c: ir_type.Type_Definition.isInst(c) and c.reference, self.children))
        map(lambda c: types.append(c), filter(Class_Reference.isInst, self.children))
        map(lambda t: types.append(t.ctype), filter(ir_variable.Variable.isInst, self.children))

        return sorted(list(set(map(lambda t: t.PackageName(), filter(isLocalType, types)))))
