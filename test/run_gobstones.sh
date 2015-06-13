#!/bin/bash
INTERP=python    # for the standard Python implementation
#INTERP=python2.3  # 2.3 version
#INTERP=pypy      # PyPy
TEST_DIR="$( dirname "${BASH_SOURCE[0]}" )"
GBS_OPTS="--no-liveness --no-print-board "$3

## Interpret directly
$INTERP $TEST_DIR/../gbs.py $GBS_OPTS $1 --from $2 --silent #2>/dev/null

## Dump bytecode and interpret
#$INTERP $TEST_DIR/../gbs.py $GBS_OPTS $TEST_DIR/examples/test.gbs --asm $TEST_DIR/examples/test.gbo --style compact --silent
#$INTERP $TEST_DIR/../gbs.py $GBS_OPTS $TEST_DIR/examples/test.gbo --from $TEST_DIR/empty.gbb --to $TEST_DIR/examples/out_py.gbb --silent #2>/dev/null

## JIT compiler 
#$INTERP $TEST_DIR/../gbs.py --jit $GBS_OPTS $TEST_DIR/examples/test.gbs --from $TEST_DIR/empty.gbb --to $TEST_DIR/examples/out_py.gbt --silent #2>/dev/null

## Dump bytecode + JIT compiler
#$INTERP $TEST_DIR/../gbs.py $GBS_OPTS $TEST_DIR/examples/test.gbs --asm $TEST_DIR/examples/test.gbo --style compact --silent
#$INTERP $TEST_DIR/../gbs.py $GBS_OPTS $TEST_DIR/examples/test.gbo --from $TEST_DIR/empty.gbb --jit --to $TEST_DIR/examples/out_py.gbb --silent #2>/dev/null
