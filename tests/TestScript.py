from TestOperation import TestOperation
from test_utils import combine_args
import functools
import re

class TestScript(object):
    
    def __init__(self, possible_args={}):
        self.cases = combine_args(possible_args)
    
    def name(self):
        return self.__class__.__name__
    
    def build_tests(self):
        return [self.build_test(c) for c in self.cases]
    
    def build_test(self, args):
        gbs_code, nretvals, py_code = self.gbs_code(), self.nretvals(), self.py_code
        if not self.has_return(gbs_code):
            nretvals = 1
            py_code = lambda args:True
            gbs_code += "\n return(True)"
        return (TestOperation(self.name(), args, nretvals, gbs_code, args), functools.partial(py_code, args))
    
    def has_return(self, gbs_code):
        match = re.search("return\([^\)]*\)", gbs_code)
        return not match is None
    
    def nretvals(self):
        return 1
    
    def gbs_code(self):
        return ""
    
    def py_code(self, args):
        return True
    
