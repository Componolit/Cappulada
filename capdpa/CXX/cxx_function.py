import cxx

class Function(cxx.Base):

    def __init__(self, name, symbol, arguments=None, return_type=None):
        super(Function, self).__init__()
        self.name = name
        self.symbol = symbol
        self.arguments = arguments or []
        self.return_type = return_type # or void
