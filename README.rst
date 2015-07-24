# PyGobstones-Lang
PyGobstones-Lang contains the implementation for Gobstones 3 and XGobstones languages.

Developers :
* Pablo Barenbaum
* Ary Pablo Batista

## Usage

```
./gbs.py <gobstonesFile> [<boardFile>] [--language (gobstones|xgobstones)] [moreOptions]
```

These are the available options:
```
Options:
  [--from] board.{gbb,gbt,tex}  Run the program in the given board file
  --to board.{gbb,gbt,tex}      Save the result in the given board file
  --size <width> <height>       Size of the input board when randomized
  --language gobstones          Uses the Gobstones 3.0's interpreter
  --language xgobstones         Uses the XGobstones 1.0's interpreter
  --pprint                      Pretty print source code
  --print-ast                   Print the abstract syntax tree
  --print-asm                   Print the code for the virtual machine
  --asm output.gbo              Generate virtual machine code
  --lint {lax,strict}           Strictness of the lint stage (default: strict)
  --no-typecheck                Don't do type inference
  --no-liveness                 Don't do live variable analysis
  --no-print-board              Don't output the result
  --no-print-retvals            Don't output the return values
  --compact                     Use compact format for dumping .gbb and .gbo files
```
