class TestOperation(object):
    
    def __init__(self, name, args, nretvals, code, replace={}):
        self.__name__ = name
        self.args = args
        self.nretvals = nretvals
        for k, v in replace.items():
            code = code.replace('@' + k, str(v))
        self.code = code
        
    def name(self):
        return self.__name__
        
    def __repr__(self):
        return "%s(%s)" % (self.name(), self.args)