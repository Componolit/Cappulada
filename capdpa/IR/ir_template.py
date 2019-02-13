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

    def __recursive_instantiation(self, entity):
        if isinstance(entity, ir_type.Type_Reference_Template):
            template = self.GetRoot()[entity.FullyQualifiedName()[1:]]
            if template:
                instance = template.instantiate(entity)
                if instance not in template.parent.children:
                    index = template.parent.children.index(template) + template.parent_index
                    template.parent.children.insert(index, instance)
                    template.parent_index += 1
            else:
                # Template not in tree, cannot instantiate
                pass

    def __replace(self, entity, resolves):
        for attr in ["children", "parameters", "arguments"]:
            if hasattr(entity, attr):
                for c in getattr(entity, attr):
                    if c.name in resolves.keys():
                        if not c.variadic:
                            getattr(entity, attr)[getattr(entity, attr).index(c)] = self.__resolve_type(c, resolves)
                        else:
                            getattr(entity, attr).extend(c)
                    self.__replace(c, resolves)
        for attr in ["ctype", "return_type"]:
            if hasattr(entity, attr):
                if hasattr(getattr(entity, attr), "name") and getattr(entity, attr).name in resolves.keys():
                    setattr(entity, attr, self.__resolve_type(getattr(entity, attr), resolves))
                self.__replace(getattr(entity, attr), resolves)
        if hasattr(entity, "size"):
            if hasattr(entity.size, "name") and entity.size.name in resolves.keys():
                entity.size = resolves[entity.size.name].value
        self.__recursive_instantiation(entity)

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
            if name == "Class":
                name = arg.name.PackagePath()[-1]
            if Template_Reference.isInst(arg):
                name += arg.postfix()
            if ir_type.Type_Literal.isInst(arg):
                name += "_" + str(arg.value)
            idlist.append(name)
        return "_T_{}".format(
                "_".join(map(self.ConvertName, idlist)))

