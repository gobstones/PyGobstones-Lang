from language.programWorker import *
from common.tools import tools
from lang.gbs_board import Board
import common.utils
import common.i18n as i18n
import lang
import logging

class GUIExecutionAPI(lang.ExecutionAPI):
    
    def __init__(self, communicator):
        self.comm = communicator
    
    def read(self):
        self.comm.send('READ_REQUEST')
        message = self.comm.receive()
        if message.header != 'READ_DONE': assert False
        return message.body        
    
    def show(self, board):
        self.comm.send('PARTIAL', tools.board_format.to_string(board))
    
    def log(self, msg):
        self.comm.send('LOG', msg)    


class GobstonesWorker(ProgramWorker):

    def prepare(self):
        self.api = GUIExecutionAPI(self.communicator)                
    
    def start(self, filename, program_text, initial_board_string, run_mode, gobstones_version="xgobstones"):
        board = tools.board_format.from_string(initial_board_string)
        
        if run_mode == GobstonesWorker.RunMode.ONLY_CHECK:
            options = lang.GobstonesOptions(lang_version=gobstones_version, check_liveness=True, lint_mode="strict")
        else:
            options = lang.GobstonesOptions(lang_version=gobstones_version)
        self.gobstones = lang.Gobstones(options, self.api)
        
        try:
            if run_mode == GobstonesWorker.RunMode.FULL:
                self.success(self.gobstones.run(filename, program_text, board))
            else:
                # Parse gobstones script
                self.gobstones.api.log(i18n.i18n('Parsing.'))
                gbs_run = self.gobstones.parse(filename, program_text)            
                assert gbs_run.tree
                # Check semantics, liveness and types
                self.gobstones.check(gbs_run.tree)
                self.success()
        except Exception as exception:
            self.failure(exception)
    
    def success(self, gbs_run=None):
        if gbs_run is None:
            self.communicator.send('OK', (None, None))
        else:
            self.communicator.send('OK', (tools.board_format.to_string(gbs_run.final_board), gbs_run.result))
    
    def failure(self, exception):
        if hasattr(exception, 'area'):
            self.communicator.send('FAIL', (exception.__class__, (exception.msg, exception.area)))
        elif hasattr(exception, 'msg'):
            self.communicator.send('FAIL', (exception.__class__, (exception.msg, )))
        else:
            self.communicator.send('FAIL', (common.utils.GobstonesException, (str(exception),)))
