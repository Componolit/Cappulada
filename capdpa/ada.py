
class Specification(object):

    def __init__(self, name, text):
        self.name = name
        self.text = text

    def Text(self):
        return self.text

    def FileName(self):
        return "-".join(n.lower() for n in self.name) + ".ads"
