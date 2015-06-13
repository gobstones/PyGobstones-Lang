from AutoGobstonesTest import AutoGobstonesTest
from TestCase import TestCase
from test_utils import unzip

class AutoTestCase(TestCase):
    
    def __init__(self, name="AutoTestCase"):
        super(AutoTestCase, self).__init__(name)
    
    def prepare(self):
        pass
    
    def program_for(self, gobstones_operations):
        pass
    
    def get_test_groups(self):
        return []
    
    def get_gobstones_tests(self):
        tests = []
        for tgroup in self.get_test_groups():
            ops, pyfs = unzip(tgroup) 
            tests.append(AutoGobstonesTest(self.program_for(ops), pyfs, self.gobstones_parameters()))
        return tests