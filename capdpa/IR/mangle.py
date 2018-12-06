class Namedb:

    def __init__ (self):

        self.db = []

    def Query (self, name):

        index = self.db.index (name)
        tag   = str(index - 1) if index > 0 else ""
        return "S" + tag + "_"

    def Get (self, name, entity):

        result = ""

        # Strip off package namespace, as this is only known internally
        stripped = name[1:]

        # Find longest match in database
        last = len(stripped)
        while not stripped[0:last] in self.db and last > 0:
            last -= 1

        if last > 0:
            result += self.Query (stripped[0:last])

        # Add new names to db
        for i in range(1, len(stripped) + 1):
            if not stripped[0:i] in self.db:
                self.db.append (stripped[0:i])

        # Handle all other parts as normal
        for i in stripped[last:]:
            result += str(len(i)) + i

        if entity == "__constructor__":
            result += "C1"
        elif not entity or entity == "Class":
            pass
        else:
            result += str(len(entity)) + entity

        # All elements of name have been replaced by reference
        fully_compressed = last > 0 and last == len(stripped)

        # At least one component and not fully compressed name
        nested = len(stripped) > 0 and not fully_compressed

        return "{nesting}{result}{end}".format(nesting = "N" if nested else "",
                                               result  = result,
                                               end     = "E" if nested else "")
