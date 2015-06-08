#
# Copyright (C) 2011-2013 Pablo Barenbaum <foones@gmail.com>,
#                         Ary Pablo Batista <arypbatista@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import os

LangDir = os.path.dirname(__file__)
GbsMacrosDir = os.path.join(LangDir, 'macros')


import common.i18n as i18n
import json
from common.utils import GobstonesException

import lang.gbs_io
import lang.gbs_parser
import lang.gbs_mexpl
import lang.gbs_lint
import lang.gbs_liveness
import lang.gbs_vm
import lang.jit.gbs_jit
import lang.gbs_pprint
import lang.gbs_infer
import lang.gbs_compiler
import lang.gbs_board
import lang.gbs_optimizer
from lang.grammar import GbsGrammarFile, XGbsGrammarFile
from lang.board.fmt_json import JsonBoardFormat
from lang.gbs_api import GobstonesOptions, GobstonesRun, ExecutionAPI

class Gobstones(object):

    def __init__(self, options=GobstonesOptions(), api=ExecutionAPI()):
        self.api = api
        self.options = options

        # Compiler pipeline methods
        self.explode_macros = lang.gbs_mexpl.mexpl
        self.lint = lang.gbs_lint.lint
        self.check_live_variables = lang.gbs_liveness.check_live_variables
        self.typecheck = lang.gbs_infer.typecheck
        self.compile_program = lang.gbs_compiler.compile_program

        if self.options.jit:
            self.make_runnable = lang.jit.gbs_jit.JitCompiledRunnable
        else:
            self.make_runnable = lang.gbs_vm.VmCompiledRunnable


    def _parse(self, program_text, filename):
        if program_text == "":
            raise GobstonesException(i18n.i18n("Cannot execute an empty program"))

        return lang.gbs_parser.parse_string_try_prelude(program_text, filename, grammar_file=self.options.get_lang_grammar())

    @classmethod
    def random_board(cls, size=None):
        if size is None:
            board = lang.gbs_board.Board()
            board.randomize_full()
        else:
            board = lang.gbs_board.Board(size)
            board.randomize_contents()
        return board

    def check(self, tree):
        # Check semantics
        self.api.log(i18n.i18n('Performing semantic checks.'))
        self.lint(tree, strictness=self.options.lint_mode)
        # Check liveness
        if self.options.check_liveness:
            self.check_live_variables(tree)
        # Check types [TODO]
        # self.typecheck(tree, self.options.check_types)

    def parse(self, filename, program_text):
        # Parse gobstones script
        self.api.log(i18n.i18n('Parsing.'))
        tree = self._parse(program_text, filename)
        assert tree
        # Explode macros
        self.api.log(i18n.i18n('Exploding program macros.'))
        self.explode_macros(tree)
        return GobstonesRun().initialize(tree)

    def compile(self, filename, program_text):
        gbs_run = self.parse(filename, program_text)
        tree = gbs_run.tree
        # Check semantics, liveness and types
        self.check(tree)
        # Optimize program
        if self.options.optimize:
            self.api.log(i18n.i18n('Optimizing.')) #[TODO] i18n
            lang.gbs_optimizer.optimize(tree)
        # Compile program
        self.api.log(i18n.i18n('Compiling.'))
        gbs_run.compiled_program = self.compile_program(tree)
        return gbs_run

    def run_object_code(self, compiled_program, initial_board):
        # Make runnable
        runnable = self.make_runnable(compiled_program)
        # Run
        self.api.log(i18n.i18n('Starting program execution.'))
        rtn_vars, final_board = runnable.run(initial_board.clone(), self.api)
        gbs_run = GobstonesRun().initialize(None, compiled_program, initial_board, final_board.value, runnable, rtn_vars)
        return gbs_run

    def run(self, filename, program_text, initial_board):
        gbs_run = self.compile(filename, program_text)
        return gbs_run.merge(self.run_object_code(gbs_run.compiled_program, initial_board))


""" Utilities """

GobstonesKeys = lang.gbs_io.GobstonesKeys
Board = lang.gbs_board.Board
pretty_print = lang.gbs_pprint.pretty_print
