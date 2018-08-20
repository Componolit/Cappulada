
class Function:

    def __init__(self, name, symbol, arguments=None, return_type=None):
        self.name = name
        self.symbol = symbol
        self.arguments = arguments or []
        self.return_type = return_type # or void
