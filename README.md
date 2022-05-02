# KarkelLang
A programming language with an intepreter and a compiler written in a functional style using python for a school assigment.

## How to use it
A short segement about how to use the intepreter and compiler and how to write program supported by example code with comments.

### Compiler and Interpeter usage

```sh
# Python version 3.10.x is required!

# Install the package
pyhton3.10 -m pip install -e .

# Installs For using the compiler output execution (optional)
sudo apt-get update
sudo apt install qemu-user
sudo apt install gcc-arm-linux-gnueabi
 
# For the interpreter
python3.10 ./KarkelLang.py [input file directory] --interpret

# For the compiler, compiles an .asm and .elf file 
# It runs the output .elf in  arm-qemu emulator
python3.10 ./KarkelLang.py [input file directory] --compile [output file]

# Compiling KarkelLang with makefiles and running the c++ unittest
Make run

```

### Example code

This function calculates the modulo of ```100 % 21``` by implementing it's own divide and modulo.
```c
                                                
& divide [# left, # right ] X #                   
<
                                                ~Function Declaration, return int~
                                                ~Int assigment~
    # quotient <- 0!
                                                ~While Loop [left > right]~                              
    O left <>> right                              
    <
                                                ~Minus operator reassignment~
        left <- left - right!
                                                ~Plus operator reassignment~                     
        quotient <- quotient + 1!                
    >
                                                ~Return Value~
    quotient -> !                                 
>
                                                
& modulo [# left, # right ] X #                   
<
                                                ~Function Declaration, return int~
                                                ~Multiply operator with function call~ 
    # decrement <- right * divide[left, right]!   
                                                ~Minus operator reassignment~              
    decrement <- left - decrement!                
                                                ~Return Value~
    decrement -> !                                
>

& Main[] X #                                      
<
                                                ~Main Function Declaration~
                                                ~Function call assignment int~
    # num <- modulo[100, 21]!  
                                                ~Return value~                   
    num -> !                                      
>

```



### Language features

- [Integers](tests/test-int-operator-multiply-1.arw), [Chars](tests/test-print-char.arw), [Strings(interpreter only)](tests/test-string-add-3.arw) and [Arrays(interpreter only)](tests/test-array-1.arw)
- If statements (Example in [test-if-statement-3.arw, line 3](./tests/test-if-statement-3.arw))
- While loops (Example in [test-while-loop-2.arw, line 6 and 8](./tests/test-while-loop-2.arw))
- Function calls (Example in [modulo.arw, line 14 and 21](./tests/modulo.arw))
  - This includes creating your own functions
  - And calling functions within functions
  - Multiple functions per file
  - For the interpreter a theoretical unlimited amount of parameters and for the arm compiler, 3 parameters
- Multiple variable scopes (Example in [test-fibonachi.arw, line 4](./tests/fibonachi.arw))
- Detailed Error messages

### Requirements

- Classes with inheritance ([astNodes.py](./astNodes.py))
- Object printing for all classes using JSON.
- Type annotated
- Uses higher order functions
  - map
    - [compiler.py](./compiler.py) 
      - line 432, compileFunctionBody
      - line 452, compileFunctionDeclareNode
      - line 461, generatePrint
      - line 513, compilerRun
    - [interpreter.py](./interpreter.py)
      - line 567, ExecuteFunctionCallNode
    - [lexer.py](./interpreter.py)
      - line 100, lexer
  - reduce
    - [compiler.py](./compiler.py) 
      - line 496, returnFile
  - zip
    - [interpreter.py](./interpreter.py)
      - line 563, ExecuteFunctionCallNode
      - line 566, ExecuteFunctionCallNode
- Multiple functions per file [exmaple](tests/modulo.arw)
- Calling functions within functions [example](tests/test-fibonachi.arw)


### Turing completeness

This language has a default flow of control, can store states, has conditional execution and repetition, which makes it able to execute/replicate the results of turing programs which makes it turing complete. 

## List of compiler requirements

### Must haves

#### Criteria

* The Code is commented with docstrings
* The repo contains a well written readme
* The code has been written in a functional style
* The code is turing complete, see [Turing completeness](#Turing_completeness)
* The language supports loops, see [modulo.arw, line 4](tests/modulo.arw)
* Classes with inheritance ([astNodes.py](./astNodes.py))
* Object printing for all classes using JSON. Try: ```python .\KarkelLang.py .\tests\modulo.arw --print```

#### Functionalities

* Compiler compiles multiple functions to assembly for ARM, see [modulo.arw](tests/modulo.arw) as an example file
* A unit test has been written in C++, see the [unittester.cpp](unittester.cpp) for the c++ unit test
* A Makefile that compiles the compiler asm and the c++ unittest enviroment, see the [Makefile](Makefile)
* Example files for testing the functionality of the language. See the folder [tests](tests) and see the file [RunTests.py](RunTests.py) for the corresponding Unit tests.
* The example files include multiple edge cases for instantiating variables with different kinds of  operators and calling functions with different kinds of arguments and running loops with different kinds of conditions in recursive and non-recursive ways.

### Should/Could haves
  * Most of the language feratures can be derived from the test files or the Modulo example earlier in this readme.
  * Comments are supported and are compiled inside the asm files. run ```python ./RunTests.py``` and check [modulo.asm](ASM-output/modulo_test.asm) for comments inside the assembler. Also comments with line numbers for the corresponding sequences are being automatically generated to make it more udnerstandable what's happening.
  * Just like the Interpreter and the Parser the compiler also supports error handling, though errors are unlikely to happen if the file succesfully passed the Parser.

