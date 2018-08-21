class NoSerializationDefined: pass

class Base(object):

    def __init__(self): pass

    def AdaSpecification(self):
	raise NoSerializationDefined
