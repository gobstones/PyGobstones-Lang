from TestCase import TestCase
from test_utils import read_file_lines, module_dir
from GobstonesRunner import run_gobstones
import os

class FileTestCase(TestCase):
    
    def __init__(self, parent, filename):
        lines = read_file_lines(filename)
        self.filename = filename
        self.parent = parent
        self.annotations, self.code = self.extract_annotations(lines)    
    
    def name(self):
        return os.path.split(self.filename)[-1]
    
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
        for res, index in zip(results, range(len(results))):
            self.parent.assertTrue(not res[1] in ["True", "False"] or res[1] == "True", "FileTestCase %s failed in the assertion number %s" % (self.name(), index))
    
    def run(self):
        if "board" in self.annotations.keys():
            if not self.annotations["board"].value is None:
                board = os.path.join(module_dir(self), self.annotations["board"].value)
            else:
                board = os.path.join(module_dir(self), self.filename[:-4] + ".gbb") 
        else:
            board = module_dir(self) + "/boards/empty.gbb"
        if not os.path.exists(board):
            raise Exception("Board file does not exist")
        results = run_gobstones(self.filename, board)
        if results[0] == "OK":
            if self.annotation_present("assert"):
                self.check_assert(results[1])
        elif results[0] == "ERROR":
            self.parent.fail(results[1])
        
        
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
        
class AnnotationException(Exception):
    pass