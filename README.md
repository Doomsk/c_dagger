# C†
Intermediate quantum programming language repository. 
We are under development. 
Please refer to [C†'s page](https://cdagger.com) for its documentation.

Up to this date, we have been able to provide the syntax and parsing it for most of what we think is enough for testing purposes.

## How to test the parser
We advice you to start a new environment to test the language.
It is still in development and may be unstable.

After creating a new env, you need to install `regex`:

```pip install regex```

You can open Jupyter Notebook or other IDE of your choice and type the following:

```
import gpp.gpp_yacc as g

code = """factorial: sets [*v1] as v1
                     multiplies [$n]_1...v1 as v2
                     uses [v2]"""
g.parse(code)
```

## How to get involved
Please contact [Doomsk](https://github.com/Doomsk) on [Twitter](https://twitter.com/byDooms).
Hopefully there will be much better ways to approach this project soon.

## This repo seems a mess! (for now)
Don't worry, we're in constant evolution! 
Things will get better when the language gets more mature and more people get involved.
 