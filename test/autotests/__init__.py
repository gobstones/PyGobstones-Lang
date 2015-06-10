import itertools
import random
import functools
from AutoGobstonesTest import AutoGobstonesTest
from test_logger import log
from test_utils import *
from GobstonesRunner import run_gobstones
from TestCase import TestCase
from GobstonesTest import GobstonesTest
from AutoTestCase import AutoTestCase
from TestOperation import TestOperation
from TestScript import TestScript
import os
# Tests

class XGbsTestScript(TestScript):
    pass

class TestOpMapping(XGbsTestScript):

    def __init__(self):
        super(TestOpMapping, self).__init__({"length": [5,10,20], "operation": BINOPS.keys()})
        
    def gbs_code(self):
        return '''
            xs := nats(1, @length)
            ys := nats(@length, 1)
            zs := []
            while(not isEmpty(xs)) {
                zs := zs ++ [head(xs) @operation head(ys)]
                xs := tail(xs)
                ys := tail(ys)
            }
            return(zs)
        '''    
        
    def pyresult(self, args):
        xs = nats(1, args["length"])
        ys = nats(args["length"], 1)
        zs = []
        while (not isEmpty(xs)):
            zs = zs + [binop(args["operation"], head(xs), head(ys))]
            xs = tail(xs)
            ys = tail(ys)
        return zs
    

class TestOpInject(XGbsTestScript):
    
    def __init__(self):
        super(TestOpInject, self).__init__({"length": [5,10,20], "operation": BINOPS.keys()})
    
    def gbs_code(self):
        return '''
            xs := nats(1, @length)
            ys := nats(@length, 1)
            res := 0
            while(not isEmpty(xs)) {
                res := res + (head(xs) @operation head(ys))
                xs := tail(xs)
                ys := tail(ys)
            }
            return(res)
        '''
        
    def pyresult(self, args):
        xs = nats(1, args["length"])
        ys = nats(args["length"], 1)
        res = 0
        while (not isEmpty(xs)):
            res += binop(args["operation"], head(xs), head(ys))
            xs = tail(xs)
            ys = tail(ys)
        return res
    
    
class TestEnumeration(XGbsTestScript):
    def __init__(self):
        super(TestEnumeration, self).__init__({"list": self.generate_cases(20)})
        
    def generate_cases(self, n):
        types = [COLORS, DIRS, BOOLS]

        def gen_case():
            vals = types[randint(len(types))]            
            return [vals[randint(len(vals))] for _ in range(randint(16) + 4)]  
        
        cases = []
        for _ in range(n):
            cases += ["[%s]" % (", ".join(gen_case()),)]
        return cases
        
    def nretvals(self):
        return 1
        
    def gbs_code(self):
        return '''
            last := head(@list)
            first_ocurr := 0
            foreach i in @list {
                if (i == last) {
                    first_ocurr := first_ocurr + 1
                }
            }
            return(first_ocurr)
        '''
        
    def pyresult(self, args):
        vals = args["list"][1:-1].split(", ")
        return vals.count(vals[0])

    
class TestListGenerator(XGbsTestScript):
    def __init__(self):
        super(TestListGenerator, self).__init__({"low": [1, 11, 33], "high": [11, 51, 22]})
    
    def nretvals(self):
        return 7
    
    def gbs_code(self):
        return '''
            xs := [@low..@high]
            ys := [@low,@low+1..@high]
            zs := [@high,@high-1..@low]
            ws := [@low,@low+5..@high]
            vs := [@high, @high-5..@low]
            us := [@low,@low+9..@high]
            ts := [@high, @high-9..@low]            
            return(ts, us, vs, ws, xs, ys, zs)
        '''
        
    def pyresult(self, args):
        xs = range(args['low'], args['high']+1)
        ys = range(args['low'], args['high']+1, 1)
        zs = range(args['high'], args['low']-1, -1)
        ws = range(args['low'], args['high']+1, 5)
        vs = range(args['high'], args['low']-1, -5)
        us = range(args['low'], args['high']+1, 9)
        ts = range(args['high'], args['low']-1, -9)
        return ts, us, vs, ws, xs, ys, zs
    
    
    
class TestRepeat(XGbsTestScript):
    def __init__(self):
        super(TestRepeat, self).__init__({"times": randomIntList(5, 20)})
    
    def nretvals(self):
        return 1
    
    def gbs_code(self):
        return '''
            count := 0
            repeat (@times)
             { count := count + 1 }
            return(count)
        '''
        
    def pyresult(self, args):
        return args["times"]
    
    
    
class TestForeachSeq(XGbsTestScript):
    def __init__(self):
        numbers = randomList(lambda i: "[" + ",".join(map(str, randomIntList(10))) + "]", 5)
        super(TestForeachSeq, self).__init__({"numbers": numbers})
    
    def nretvals(self):
        return 1
    
    def gbs_code(self):
        return '''
            res := 0
            foreach n in @numbers
             { res := res*10 + n }
            return(res)
        '''
        
    def pyresult(self, args):
        res = 0
        ns = args["numbers"][1:-1].split(",")
        for n in map(int, ns):
            res = res*10 + n
        return res 
    
    
TESTS_GROUPS = group(flatten([cls().build_tests() for cls in XGbsTestScript.__subclasses__()]), 128)
TEST_DIR = os.path.dirname(os.path.dirname(__file__))
THIS_TEST_DIR = os.path.dirname(__file__)

class XGbsAutoTestCase(AutoTestCase):
    
    def __init__(self):
        super(XGbsAutoTestCase, self).__init__("XGbsAutoTestCase")
        self.name = "Automatic Test Cases for XGobstones"
    
    def prepare(self):
        copy_file(THIS_TEST_DIR + "/Biblioteca.gbs", TEST_DIR + "/examples/Biblioteca.gbs")
    
    def get_test_groups(self):
        return TESTS_GROUPS
    
    def program_for(self, gobstones_operations):
        variables = []
      
        def expr_eval(i, e):
            if isinstance(e, TestOperation):
                if e.nretvals == 1: 
                    variables.append('x_%i' % (i,))
                    return 'x_%i := f0_%i()' % (i, i,)
                else:
                    vs = ['x_%i_%i' % (i, j) for j in range(e.nretvals)]
                    variables.extend(vs)
                    return '(%s) := f0_%i()' % (','.join(vs), i,)
            else:
                variables.append('x_%i' % (i,))
                return 'x_%i := %s' % (i, e)
          
        R = range(len(gobstones_operations))
        prog = []
        for i, e in zip(R, gobstones_operations):
            if isinstance(e, TestOperation):
                prog.append('function f0_%i() {' % (i,))
                prog.append(e.code)
                prog.append('}')
        prog.append('t.program {')
        prog.append(''.join(['  %s\n' % (expr_eval(i, e),) for i, e in zip(R, gobstones_operations)]))
        prog.append('  return (%s)\n' % (', '.join(variables),))
        prog.append('}\n')
        return '\n'.join(prog)