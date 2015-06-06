import sys
import os
import os.path
import importlib
import inspect
from GobstonesRunner import run_gobstones
from TestCase import TestCase
from GobstonesTest import GobstonesTest
from test_logger import log
from test_utils import read_file_lines, is_module, parent_dir, module_dir, run_cmd, delete_files_in_dir, dir_has_tests
import autotestsGbs3
import autotests

def cleanup():
    clean_dir = os.path.join(parent_dir(__file__), "examples")
    delete_files_in_dir(clean_dir, ["README"])

class TestException(Exception):
    pass


class AnnotationException(TestException):
    pass


class AnnotationBuilder(object):
    
    def build(self, s):        
        self.check_malformed(s)
        splitted = s.split(Annotation.ANNOTATION_SEQ)[1].split("=")
        if len(splitted) == 1:
            return Annotation(splitted[0])
        else:
            return Annotation(splitted[0], splitted[1])        
        
    def check_malformed(self, s):
        if not s.startswith(Annotation.ANNOTATION_SEQ):
            raise AnnotationException() 


class Annotation(object):

    ANNOTATION_SEQ = "#!"
    
    def __init__(self, key, value=None):
        self.key = key
        self.value = value


class GobstonesTest(object):
    
    def name(self):
        return self.__class__.__name__


class GobstonesFileTest(GobstonesTest):
    
    def __init__(self, filename):
        lines = read_file_lines(filename)
        self.filename = filename
        self.annotations, self.code = self.extract_annotations(lines)    
    
    def name(self):
        return self.filename
    
    def extract_annotations(self, lines):
        annotations = {}
        code = []
        for l in lines:
            if Annotation.ANNOTATION_SEQ in l.strip():
                annotation = AnnotationBuilder().build(l.strip())
                annotations.update({annotation.key:annotation})
            else:
                code.append(l)
        return (annotations, code)
    
    def annotation_present(self, annotation_name):
        return annotation_name in self.annotations.keys()
    
    def check_assert(self, results):
        passed = True
        for res in results:
            passed = passed and (not res[1] in ["True", "False"] or res[1] == "True")
        return passed
    
    def run(self):
        if "board" in self.annotations.keys():
            if not self.annotations["board"].value is None:
                board = os.path.join(module_dir(self), self.annotations["board"].value)
            else:
                board = os.path.join(module_dir(self), self.filename[:-4] + ".gbb") 
        else:
            board = os.path.join(parent_dir(__file__), "boards/empty.gbb")
        results = run_gobstones(self.filename, board)
        if results[0] == "OK":
            passed = True
            if self.annotation_present("assert"):
                passed = passed and self.check_assert(results[1])
            
            if passed:
                return "PASSED"
            else:
                return "FAILED"
        else:
            return results[0]
        
        def check_assert(self, results):
            pass
                    
class FileTestCase(TestCase):
        
    def get_gobstones_tests(self):
        PATH = os.path.join(parent_dir(__file__), self.name)
        return [ GobstonesFileTest(os.path.join(PATH, f)) for f in os.listdir(PATH) if ".gbs" in f and self.is_test_file(PATH, f)]        
    
    def is_test_file(self, path, filename):
        return os.path.isfile(os.path.join(path, filename)) and filename.startswith("test") and filename.endswith(".gbs")
            

class Tester(object):
    
    def test(self):
        test_cases = self.get_test_cases()
        
        passed = 0
        failed = 0
        errors = 0
        for test_case in test_cases:
            test_case.prepare()
            test_case.run()
            print repr(test_case)
            passed += test_case.passed
            failed += test_case.failed
            errors += test_case.errors
            cleanup()
            
        print "Total:\n--passed: %s\n--failed: %s\n--errors: %s\n" % (passed, failed, errors)
        
    def get_test_cases(self):
        return self.get_file_test_cases() + [autotests.AutoTestCase(), autotestsGbs3.AutoTestCaseGbs3()]
        
    def get_file_test_cases(self):
        PATH = os.path.split(os.path.realpath(__file__))[0]
        return [self.get_module_testcase(f) for f in os.listdir(PATH) if not os.path.isfile(os.path.join(PATH, f)) and is_module(f) and dir_has_tests(f)]

    def get_module_testcase(self, m):
        return FileTestCase(m)
#         module = importlib.import_module(m)
#         for name, obj in inspect.getmembers(module):
#             if inspect.isclass(obj) and issubclass(obj, TestCase):
#                 return obj

if __name__ == "__main__":
    Tester().test()            