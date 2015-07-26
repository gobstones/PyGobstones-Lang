from TestCase import TestCase
import os
from FileTestCase import FileTestCase
from test_utils import parent_dir


class FileBundleTestCase(TestCase):

    def get_tests_directory(self):
        module = self.__class__.__module__.split(".")[-2]
        return os.path.join(parent_dir(__file__), module)

    def get_gobstones_tests(self):
        PATH = self.get_tests_directory()
        return [ FileTestCase(self, os.path.join(PATH, f)) for f in os.listdir(PATH) if ".gbs" in f and self.is_test_file(PATH, f)]

    def is_test_file(self, path, filename):
        return os.path.isfile(os.path.join(path, filename)) and filename.startswith("test") and filename.endswith(".gbs")