import subprocess
import os

class GobstonesRunner(object):

    def lang_path(self):
        return os.path.dirname(__file__) + "/../pygobstoneslang.py"
        #return "pygobstones-lang"

    def base_parameters(self):
        return "--no-print-board --silent --test-suite"

    def run(self, filename, board_file, parameters=""):
        command = (self.lang_path() + " %s %s %s %s") % (
            filename, board_file, self.base_parameters(), parameters)
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
            )

        #Launch the shell command:
        output, error = process.communicate()
        output = output.replace("\r", "")
        result = output.split('\n')
        while len(result) > 0 and result[-1] == '':
            result = result[:-1]

        output = None
        if len(result) == 0 or result[-1] != 'OK':
            output = ('ERROR', error)
        else:
            result = result[:-1]
            dic = []
            var, val = "", ""
            for res in result:
                if res.count("->") > 0:
                    dic.append((var.strip(' \t\r\n'), val.strip(' \t\r\n')))
                    var, val = res.split('->')
                else:
                    val += "\n" + res
            dic.append((var.strip(' \t\r\n'), val.strip(' \t\r\n')))
            if len(dic) > 1:
                dic = dic[1:]
            else:
                dic = []
            output = ('OK', dic)

        return output


run_gobstones = GobstonesRunner().run
