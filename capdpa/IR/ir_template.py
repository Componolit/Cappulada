import ir
from copy import deepcopy

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
                if c in resolves.keys():
                    c = resolves[c]
                self.__replace(c, resolves)
        if hasattr(entity, "parameters"):
            for c in entity.parameters:
                if c in resolves.keys():
                    c = resolves[c]
                self.__replace(c, resolves)
        if hasattr(entity, "ctype"):
            if entity.ctype in resolves.keys():
                entity.ctype = resolves[entity.ctype]
        if hasattr(entity, "return_type"):
            if entity.return_type in resolves.keys():
                entity.return_type = resolves[entity.return_type]

    def InstantiateTemplates(self):
        pass

    def instantiate(self, ref):
        resolves = {t[0]:t[1] for t in zip(self.typenames, ref.arguments)}
        entity = deepcopy(self.entity)
        self.__replace(entity, resolves)
        entity.name += ref.postfix()
        return entity

class Template_Argument(ir.Base):

    def __init__(self, name):
        self.name = name
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

