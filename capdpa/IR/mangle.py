class Namedb:

    def __init__ (self):

        self.db = []

    def Get (self, parent):

        result = ""
        for i in parent[0:-1]:
            result += str(len(i)) + i

        name = parent[-1]
        if name == "__constructor__":
            result += "C1"
        else:
            result += str(len(name)) + name

        if result in self.db:
            index = self.db.index (result)
            tag   = str(index-1) if index > 0 else ""
            return "S" + tag + "_"

        self.db.append (result)
        return result
