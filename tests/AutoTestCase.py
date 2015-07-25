from AutoGobstonesTest import AutoGobstonesTest
from TestCase import TestCase
from test_utils import unzip, delete_files_in_dir, parent_dir
import os


class AutoTestCase(TestCase):

    def program_for(self, gobstones_operations):
        pass

    def get_test_groups(self):
        return []

    def get_gobstones_tests(self):
        tests = []
        test_groups = self.get_test_groups()
        for tgroup, index in zip(test_groups, range(len(test_groups))):
            ops, pyfs = unzip(tgroup)
            tests.append(AutoGobstonesTest(
                "group %s, %s tests" % (index, len(ops)),
                self,
                ops,
                self.program_for(ops),
                pyfs,
                self.gobstones_parameters()
                ))
        return tests

    def cleanup(self):
        clean_dir = os.path.join(parent_dir(__file__), "examples")
        delete_files_in_dir(clean_dir, ["README"])