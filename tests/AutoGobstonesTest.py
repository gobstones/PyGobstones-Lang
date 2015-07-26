from test_utils import unzip, temp_test_file
from GobstonesRunner import run_gobstones
import os
from TestCase import TestCase


class AutoGobstonesTest(TestCase):

    def __init__(self, name, parent, operations,
                 gbscode, pyfuncs, gbsparams=""):
        self.__name__ = name
        self.operations = operations
        self.gbscode = gbscode
        self.pyfuncs = pyfuncs
        self.gbsparams = gbsparams
        self.parent = parent
        self.assertEqual = self.parent.assertEqual
        self.fail = self.parent.fail

    def name(self):
        return self.__name__

    def run(self):
        result_to_op = []
        for op in self.operations:
            result_to_op.extend([op for x in range(op.nretvals)])
            #print "\tRunning subtest %s" % (op,)
        run_params = [
            temp_test_file(self.gbscode),
            os.path.dirname(__file__) + "/boards/empty.gbb",
            self.gbsparams
            ]
        results = run_gobstones(*run_params)
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
                for gbsval, pyval, index in zip(
                    unzip(gbsres)[1],
                    pyres,
                    range(len(pyres))
                    ):
                    self.assertEqual(
                        gbsval,
                        str(pyval),
                        ("Operation %s failed. The result %s do not match " +
                        "the expected value. " +
                        "Expected: %s. Actual: %s"
                        ) % (
                            result_to_op[index],
                            index,
                            pyval,
                            gbsval
                            )
                        )
            else:
                self.fail("The execution results count do " +
                          "not match the expected results count")
        else:
            self.fail(results[1])
