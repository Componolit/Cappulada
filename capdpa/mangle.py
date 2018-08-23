# Mangling is defined in the Itanium C++ ABI:
# https://itanium-cxx-abi.github.io/cxx-abi/abi.html#mangling

class Mangle:

    def __init__(self, function):
        self.function = function

    def ToString(self):

        package = self.function.name.PackageFull()

        # Mangled-name prefix
        result = "_Z"

        # Nested name (as we use this only for constructors, this will always
        # be nested.
        result += "N"

        for p in package:
            result += str(len(p)) + p

        # Assuming constructor type C1 - "complete object constructor"
        result += "C1"

        # E tag of <nested-name>
        result += "E"

        # parameters
        if not self.function.parameters:
            # void: 'v'
            result += "v"
        else:
            raise Exception("Return types not implemented")

        return result
