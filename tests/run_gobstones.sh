#!/bin/bash
INTERP=python    # for the standard Python implementation
#INTERP=python2.3  # 2.3 version
#INTERP=pypy      # PyPy
TEST_DIR="$( dirname "${BASH_SOURCE[0]}" )"
GBS_OPTS="--no-print-board "$3
GBS_MAIN=$TEST_DIR/../pygobstoneslang/__main__.py

RUN_GBS=$INTERP $GBS_MAIN $GBS_OPTS

## Interpret
$RUN_GBS $1 --from $2 --silent #2>/dev/null

## Dump bytecode and interpret
#$RUN_GBS $TEST_DIR/examples/test.gbs --asm $TEST_DIR/examples/test.gbo --style compact --silent
#$RUN_GBS $TEST_DIR/examples/test.gbo --from $TEST_DIR/empty.gbb --to $TEST_DIR/examples/out_py.gbb --silent #2>/dev/null

## JIT compiler 
#$RUN_GBS --jit $TEST_DIR/examples/test.gbs --from $TEST_DIR/empty.gbb --to $TEST_DIR/examples/out_py.gbt --silent #2>/dev/null

## Dump bytecode + JIT compiler
#$RUN_GBS $TEST_DIR/examples/test.gbs --asm $TEST_DIR/examples/test.gbo --style compact --silent
#$RUN_GBS $TEST_DIR/examples/test.gbo --from $TEST_DIR/empty.gbb --jit --to $TEST_DIR/examples/out_py.gbb --silent #2>/dev/null
