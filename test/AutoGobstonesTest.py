from test_utils import eqValue, unzip, temp_test_file
from GobstonesRunner import run_gobstones
from GobstonesTest import GobstonesTest
import os

class AutoGobstonesTest(GobstonesTest):

    def __init__(self, gbscode, pyfuncs):
        self.gbscode = gbscode
        self.pyfuncs = pyfuncs
        
    def run(self):
        results = run_gobstones(temp_test_file(self.gbscode), os.path.dirname(__file__)+"/boards/empty.gbb")
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
                for gbsval, pyval in zip(unzip(gbsres)[1], pyres):
                    if not eqValue(gbsval, pyval):
                        return "FAILED"
                return "PASSED"
            else:
                return "FAILED"            
        else:
            return results[0]