from test_utils import eqValue, unzip, temp_test_file
from GobstonesRunner import run_gobstones
import os
from TestCase import TestCase

class AutoGobstonesTest(TestCase):

    def __init__(self, name, parent, operations, gbscode, pyfuncs, gbsparams=""):
        self.__name__ = name
        self.operations = operations
        self.gbscode = gbscode
        self.pyfuncs = pyfuncs
        self.gbsparams = gbsparams
        self.parent = parent
        
    def name(self):
        return self.__name__
        
    def run(self):
        result_to_op = []
        for op in self.operations:
            result_to_op.extend([op for x in range(op.nretvals)])
            print "\tRunning subtest %s" % (op,)
        results = run_gobstones(temp_test_file(self.gbscode), os.path.dirname(__file__)+"/boards/empty.gbb", self.gbsparams)
        if results[0] == "OK":
            gbsres = results[1]
            pyres = []
            for f in self.pyfuncs:
                pyr = f()
                if isinstance(pyr, tuple):
                    pyres += list(pyr)
                else:
                    pyres.append(pyr)
                    
            if len(pyres) == len(gbsres):
                for gbsval, pyval, index in zip(unzip(gbsres)[1], pyres, range(len(pyres))):
                    self.parent.assertEqual(gbsval, str(pyval), "Operation %s failed. The result %s do not match the expected value. Expected: %s. Actual: %s" % (result_to_op[index], index, pyval, gbsval))
            else:
                self.parent.fail("The execution results count do not match the expected results count")      
        else:
            self.parent.fail(results[1])
