import subprocess
import os

class GobstonesRunner(object):
    
    def run(self, filename, board_file, parameters=""):
        command = os.path.dirname(__file__) + "/run_gobstones.sh %s %s \"%s\"" % (filename, board_file, parameters)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

        #Launch the shell command:
        output, error = process.communicate()
        
        result = output.split('\n')
        while len(result) > 0 and result[-1] == '': result = result[:-1]
        if len(result) == 0 or result[-1] != 'OK':
            return 'ERROR', error 
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
            return 'OK', dic
        
run_gobstones = GobstonesRunner().run