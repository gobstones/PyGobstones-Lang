import itertools
import functools
from test_logger import log
from test_utils import *
from GobstonesRunner import run_gobstones
from TestCase import TestCase
from GobstonesTest import GobstonesTest
from AutoGobstonesTest import AutoGobstonesTest
from AutoTestCase import AutoTestCase
from TestOperation import TestOperation
from test_utils import *
from TestScript import TestScript
    
# Tests

class GbsTestScript(TestScript):
    pass

class TestForeachSeq(GbsTestScript):
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

class TestRepeat(GbsTestScript):
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

class TestForeachWithRangeIterations(GbsTestScript):
    
    def __init__(self):
        super(TestForeachWithRangeIterations, self).__init__({"start_val": [1, 7, 11,21], "end_val": [21,5,13]})
    
    def gbs_code(self):
        return '''
            VaciarTablero()
            foreach i in [@start_val..@end_val] {
                Poner(Verde)
            }
            return(nroBolitas(Verde))
        '''
    
    def pyresult(self, args):
        start = args["start_val"]
        end = args["end_val"]
        if start <= end:
            return end+1 - start
        else:
            return 0
        
class TestForeachWithRangeAndDeltaIterations(GbsTestScript):
     
    def __init__(self):
        super(TestForeachWithRangeAndDeltaIterations, self).__init__({"start_val": [0, 7, 11,21], "end_val": [21,5,13], "delta": [1,-1,2,-2,3,-3]})
     
    def gbs_code(self):
        return '''
            VaciarTablero()
            foreach i in [@start_val, @start_val + @delta ..@end_val] {                
                Poner(Verde)
            }
            return(nroBolitas(Verde))
        '''
     
    def pyresult(self, args):
        start = args["start_val"]
        end = args["end_val"]
        delta = args["delta"] * 1.0
        if start == end:
            return 1
        if delta > 0 and start > end:
            return 0            
        elif delta < 0 and end > start:
            return 0        
        elif start <= end:
            return iceil((end+1 - start)/abs(delta))
        else:
            return iceil((start+1 - end)/abs(delta))
            
    
TESTS_GROUPS = group(flatten([cls().build_tests() for cls in GbsTestScript.__subclasses__()]), 128)
TEST_DIR = os.path.dirname(os.path.dirname(__file__))
THIS_TEST_DIR = os.path.dirname(__file__)

class AutoTestCaseGbs3(AutoTestCase):
    
    def __init__(self):
        super(AutoTestCaseGbs3, self).__init__("Automatic Test Cases for Gobstones 3")
    
    def prepare(self):
        copy_file(THIS_TEST_DIR + "/Biblioteca.gbs", TEST_DIR + "/examples/Biblioteca.gbs")
    
    def gobstones_parameters(self):
        return "--language gobstones"
    
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
        prog.append('program {')
        prog.append(''.join(['  %s\n' % (expr_eval(i, e),) for i, e in zip(R, gobstones_operations)]))
        prog.append('  return (%s)\n' % (', '.join(variables),))
        prog.append('}\n')
        return '\n'.join(prog)