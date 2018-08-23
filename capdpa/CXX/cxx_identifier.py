import cxx

class Identifier(cxx.Base):

    def __init__(self, name):
        super(Identifier, self).__init__()
        self.name = name

    def PackageFull(self):
        return self.name

    def PackageFullName(self):
        return ".".join(map(self.ConvertIdentifier, self.PackageFull()))

    def PackagePath(self):
        return self.name[:-1]

    def PackagePathName(self):
        return ".".join(map(self.ConvertIdentifier, self.PackagePath()))

    def PackageBaseName(self):
        return self.ConvertIdentifier(self.name[-1])
