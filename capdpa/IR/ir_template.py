import ir
import ir_function
from copy import deepcopy, copy

class UnspecifiedTemplate: pass

class Template(ir.Base):

    def __init__(self, entity, typenames, parent_index=1):
        self.entity = entity
        self.typenames = typenames
        self.name = self.entity.name
        self.parent_index = parent_index
        super(Template, self).__init__()

    def __repr__(self):
        return super(Template, self).__repr__(['parent_index'])

    def SetParent(self, parent):
        self.parent = parent
        self.entity.parent = parent

    def __replace(self, entity, resolves):
        if hasattr(entity, "children"):
            for c in entity.children:
                if c.name in resolves.keys():
                    if not c.variadic:
                        c = resolves[c.name]
                    else:
                        entity.children.extend(c)
                self.__replace(c, resolves)
        if hasattr(entity, "parameters"):
            for c in entity.parameters:
                if c.name in resolves.keys():
                    if not c.variadic:
                        c = resolves[c.name]
                    else:
                        entity.parameters.extend(resolves[c.name])
                self.__replace(c, resolves)
        if hasattr(entity, "ctype"):
            if entity.ctype.name in resolves.keys():
                ct = resolves[entity.ctype.name]
                ct.reference = entity.ctype.reference
                ct.pointer   = entity.ctype.pointer
                entity.ctype = copy(ct)
            self.__replace(entity.ctype, resolves)
        if hasattr(entity, "return_type"):
            if entity.return_type and entity.return_type.name in resolves.keys():
                entity.return_type = resolves[entity.return_type.name]
            self.__replace(entity.return_type, resolves)

    def InstantiateTemplates(self):
        pass

    def instantiate(self, ref):
        if not self.typenames[-1].variadic:
            resolves = {t[0].name:t[1] for t in zip(self.typenames, ref.arguments)}
        else:
            resolves = {t[0].name:t[1] for t in zip(self.typenames[:-1], ref.arguments[:len(self.typenames) - 1])}
            resolves[self.typenames[-1]] = ref.arguments[len(self.typenames) - 1:]
        entity = deepcopy(self.entity)
        self.__replace(entity, resolves)
        entity.name += ref.postfix()
        entity.instanceof = (self.FullyQualifiedName(), ref.arguments)
        return entity

class Template_Argument(ir.Base):

    def __init__(self, name, variadic=False, reference=False, pointer=0):
        self.name = name
        self.variadic = variadic
        self.reference = reference
        self.pointer = pointer
        super(Template_Argument, self).__init__()

class Template_Reference(ir.Base):

    # don't use this class alone, inherit from it and provide arguments

    def postfix(self):
        idlist = []
        for arg in self.arguments:
            name = arg.name.PackageBaseNameRaw()
            if Template_Reference.isInst(arg):
                name += arg.postfix()
            idlist.append(name)
        return "_T_{}".format(
                "_".join(idlist))

