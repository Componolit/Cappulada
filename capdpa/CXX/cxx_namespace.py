import cxx

class Namespace(cxx.Base):

    def __init__(self, name, namespaces=None, classes=None, constants=None, enums=None):
        super(Namespace, self).__init__()
        self.namespaces = namespaces or []
        self.classes = classes or []
