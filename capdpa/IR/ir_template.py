import ir
from copy import deepcopy

class UnspecifiedTemplate: pass

class Template(ir.Base):

    def __init__(self, entity, typenames):
        self.entity = entity
        self.typenames = typenames
        self.name = self.entity.name
        super(Template, self).__init__()

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

    def instantiate(self, ref):
        resolves = {t[0]:t[1] for t in zip(self.typenames, ref.arguments)}
        entity = deepcopy(self.entity)
        self.__replace(entity, resolves)
        entity.name += ref.postfix()
        return entity

class Template_Argument(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.__repr__() == repr(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Template_Argument(name={})".format(
                self.name)

    def __hash__(self):
        return hash(self.__repr__())

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

