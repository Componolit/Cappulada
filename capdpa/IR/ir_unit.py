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

    def InstantiateTemplates(self):
        pass

class Unit(ir.Base):

    def UsedPackages(self):
        types = []

        isLocalType = lambda t: \
            ir_type.Type_Reference_Template.isInst(t) or \
            (t.name.PackagePath() and \
             self.FullyQualifiedName()[:len(t.name.PackagePath())] != t.name.PackagePath() and \
             t.name.PackagePath() not in [c.FullyQualifiedName() for c in self.children])

        for f in filter(ir_function.Function.isInst, self.children):
            map(lambda p: types.append(p.ctype), f.parameters)
            if f.return_type:
                types.append(f.return_type)

        map(lambda v: types.append(v.ctype), filter(ir_variable.Member.isInst, self.children))
        map(lambda t: types.append(t.reference), filter(lambda c: ir_type.Type_Definition.isInst(c) and c.reference, self.children))
        map(lambda c: types.append(c), filter(Class_Reference.isInst, self.children))
        map(lambda t: types.append(t.ctype), filter(ir_variable.Variable.isInst, self.children))

        return sorted(list(set(map(lambda t: t.PackageName(), filter(isLocalType, types)))))
