# C†

[![Join the chat at https://gitter.im/c_dagger/help](https://badges.gitter.im/c_dagger/help.svg)](https://gitter.im/c_dagger/help?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Intermediate quantum programming language repository.
We are under development.
Please refer to [C†'s page](https://cdagger.com) for its (more extensive) documentation.

Up to this date, we have been able to provide the syntax and parsing it for most of what we think is enough for testing purposes.

## How to test the parser
We advice you to start a new environment to test the language.
It is still in development and may be unstable.

After creating a new env, you need to install `regex`:

```pip install regex```

You can open Jupyter Notebook or other IDE of your choice and type the following:

```
import cdag.cdag.gpp.gpp_yacc as g

code = """factorial: sets [*v1] as v1
                     multiplies [$n]_1...v1 as v2
                     uses [v2]"""
g.parse(code)
```
You can also run one of the test C† files by typing:

```
import cdag.cdag.gpp.gpp_yacc as g

g.test(1)  # or g.test(3)
```


## How to get involved
Please contact [Doomsk](https://github.com/Doomsk) on [Twitter](https://twitter.com/byDooms).
Hopefully there will be much better ways to approach this project soon.

## Roadmap
Currently there are some open approaches we are working on:

- Prototyping ![prototyping](https://img.shields.io/badge/status-wip-orange.svg?style=flat-square)]: first attempt to write the bare minimum information for the language, i.e.: a lexer, parser, syntax tree, interpreter. All in Python and all in English for prototyping purposes.
	- Lexer ![lexer](https://img.shields.io/badge/status-ok!-brightgreen.svg?style=flat-square): writing the first lexer to get an idea how the language should look like.
	- Parser ![lexer](https://img.shields.io/badge/status-ok!-brightgreen.svg?style=flat-square): writing the first parser to understand how the syntax should look like.
	- Interpreter ![prototyping](https://img.shields.io/badge/status-wip-orange.svg?style=flat-square): writing the first interpreter to understand how the code should interact.
	- Compiler language choice ![fcomp](https://img.shields.io/badge/status-not%20started-yellow.svg?style=flat-square): choose the programming language in which C† should be seriously developed at first (C, C++, Rust?).
- First Compiler ![fcomp](https://img.shields.io/badge/status-not%20started-yellow.svg?style=flat-square): write the memory handling, choose the first bult-in actions to develop.
	- Lexer
	- Parser
	- Compiler
	- Data Analyzer: should it be Julia in the end?
- First Quantum Hardware Implementation ![fqhi](https://img.shields.io/badge/status-not%20started-yellow.svg?style=flat-square): attempt to implement some code on C† to deal with pulses and other instructions as read and write from and to quantum processors.
	- Hardware interaction: will it be Intel/ARM/FPGA/other hardware to receive data from C†?
	- Native hardware: which hardware will it be most efficient to be implemented on?
	- Instructions channel: which channel to communicate via local, lan and wan?
