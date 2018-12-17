import ir
import ir_function
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
        listattr = ["children", "parameters"]
        singleattr = ["ctype", "return_type"]
        listattr = [attr for attr in listattr if hasattr(entity, attr)]
        singleattr = [attr for attr in singleattr if hasattr(entity, attr)]
        for attr in listattr:
            for c in getattr(entity, attr):
                if c in resolves.keys():
                    if not c.variadic:
                        c = resolves[c]
                    else:
                        getattr(entity, attr).extend(c)
                self.__replace(c, resolves)
        for attr in singleattr:
            if getattr(entity, attr) in resolves.keys():
                setattr(entity, attr, resolves[getattr(entity, attr)])
            self.__replace(getattr(entity, attr), resolves)

    def InstantiateTemplates(self):
        pass

    def instantiate(self, ref):
        if not self.typenames[-1].variadic:
            resolves = {t[0]:t[1] for t in zip(self.typenames, ref.arguments)}
        else:
            resolves = {t[0]:t[1] for t in zip(self.typenames[:-1], ref.arguments[:len(self.typenames) - 1])}
            resolves[self.typenames[-1]] = ref.arguments[len(self.typenames) - 1:]
        entity = deepcopy(self.entity)
        self.__replace(entity, resolves)
        entity.name += ref.postfix()
        return entity

class Template_Argument(ir.Base):

    def __init__(self, name, variadic=False):
        self.name = name
        self.variadic = variadic
        super(Template_Argument, self).__init__()


class Template_Reference_Base(ir.Base):

    # don't use this class alone, inherit from it and provide arguments

    def postfix(self):
        idlist = []
        for arg in self.arguments:
            name = arg.name.PackageBaseNameRaw()
            if Template_Reference_Base.isInst(arg):
                name += arg.postfix()
            idlist.append(name)
        return "_T_{}".format(
                "_".join(idlist))

