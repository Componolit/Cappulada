import ir

class Identifier(ir.Base):

    def __init__(self, name):
        super(Identifier, self).__init__()
        self.name = name

    def PackageFull(self):
        return self.name

    def PackageFullName(self):
        return ".".join(map(self.ConvertName, self.PackageFull()))

    def PackagePath(self):
        return self.name[:-1]

    def PackagePathName(self):
        return ".".join(map(self.ConvertName, self.PackagePath()))

    def PackageBaseName(self):
        return self.ConvertName(self.name[-1])

    def PackageBaseNameRaw(self):
        return self.name[-1]
