class TestCase(object):
        
    def name(self):
        return self.__class__.__name__

    def __repr__(self):
        return "TestCase: %s, " % self.name
    
    def get_gobstones_tests(self):
        "Get Test Case's tests"
        return []
    
    def prepare(self):
        "Prepare the testcase to run."
        pass
    
    def gobstones_parameters(self):
        "Parameters for language implementation"
        return ""
    
    def testCases(self):
        test_cases = self.get_gobstones_tests()
        for test_case in test_cases:
            print "%s: Running test %s" % (self.name(), test_case.name())
            test_case.run()
        self.cleanup()

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def cleanup(self):
        pass