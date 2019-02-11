import ir
import ir_function
import ir_type
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

    def __resolve_type(self, ctype, resolves):
        rt = copy(resolves[ctype.name])
        rt.reference = ctype.reference
        rt.pointer   = ctype.pointer
        return rt

    def __replace(self, entity, resolves):
        if hasattr(entity, "children"):
            for c in entity.children:
                if c.name in resolves.keys():
                    if not c.variadic:
                        c = self.__resolve_type(c, resolves)
                    else:
                        entity.children.extend(c)
                self.__replace(c, resolves)
        if hasattr(entity, "parameters"):
            for c in entity.parameters:
                if c.name in resolves.keys():
                    if not c.variadic:
                        c = self._resolve_type(c, resolves)
                    else:
                        entity.parameters.extend(self.__resolve_type(c, resolves))
                self.__replace(c, resolves)
        if hasattr(entity, "ctype"):
            if hasattr(entity.ctype, "name") and entity.ctype.name in resolves.keys():
                entity.ctype = self.__resolve_type(entity.ctype, resolves)
            self.__replace(entity.ctype, resolves)
        if hasattr(entity, "size"):
            if hasattr(entity.size, "name") and entity.size.name in resolves.keys():
                entity.size = resolves[entity.size.name].value
        if hasattr(entity, "return_type"):
            if entity.return_type and entity.return_type.name in resolves.keys():
                entity.return_type = self.__resolve_type(entity.return_type, resolves)
            self.__replace(entity.return_type, resolves)

    def InstantiateTemplates(self):
        pass

    def UsedTypes(self, parent):
        types = []
        for t in self.entity.UsedTypes(parent) or []:
            types.append(t)
        return types

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

    def UsedTypes(self, parent):
        return []

class Template_Reference(ir.Base):

    # don't use this class alone, inherit from it and provide arguments

    def postfix(self):
        idlist = []
        for arg in self.arguments:
            name = arg.name.PackageBaseNameRaw()
            if Template_Reference.isInst(arg):
                name += arg.postfix()
            if ir_type.Type_Literal.isInst(arg):
                name += "_" + str(arg.value)
            idlist.append(name)
        return "_T_{}".format(
                "_".join(map(self.ConvertName, idlist)))

