class TestCase(object):
    
    def __init__(self, testcase_name):
        self.name = testcase_name
        self.passed = 0
        self.failed = 0
        self.errors = 0    

    def __repr__(self):
        output = "TestCase: %s, " % self.name
        if self.errors > 0:
            output += "ERROR."
        elif self.failed > 0:
            output += "FAILED."
        else:
            output += "OK."
        return output
    
    def get_gobstones_tests(self):
        "Get Test Case's tests"
        return []
    
    def prepare(self):
        "Prepare the testcase to run."
        pass
    
    def gobstones_parameters(self):
        "Parameters for language implementation"
        return ""
    
    def run(self):
        tests = self.get_gobstones_tests()
        self.result = {"PASSED":0, "FAILED":0, "ERROR":0}
        for test in tests:
            self.setup()
            res = test.run()
            if res == "FAILED":
                print "Failed test '%s'" % (test.name(),)
            self.result[res] += 1
            self.teardown()
        
        self.passed = self.result["PASSED"]
        self.failed = self.result["FAILED"]
        self.errors = self.result["ERROR"]

    def setup(self):
        pass
        
    def teardown(self):
        pass