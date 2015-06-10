from GobstonesTest import GobstonesTest
from TestOperation import TestOperation
from test_utils import combine_args
import functools

class TestScript(GobstonesTest):
    
    def __init__(self, possible_args):
        self.cases = combine_args(possible_args)
    
    def name(self):
        return self.__class__.__name__
    
    def build_tests(self):
        return [self.build_test(c) for c in self.cases]
    
    def build_test(self, args):
        return (TestOperation(self.nretvals(), self.gbs_code(), args), self.py_func(args))
    
    def nretvals(self):
        return 1
    
    def gbs_code(self):
        return "Skip"
    
    def py_func(self, args):
        return functools.partial(self.pyresult, args)
    
    def py_code(self, args):
        pass