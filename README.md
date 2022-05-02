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
python ./KarkelLang.py [input file directory] --interpret

# For the compiler, compiles an .asm and .elf file 
# It runs the output .elf in  arm-qemu emulator
python ./KarkelLang.py [input file directory] --compile [output file]

# Compiling KarkelLang with makefiles and running the c++ unittest
Make run

```

### Example code

This function calculates the modulo of ```100 % 21``` by implementing it's own divide and modulo.
```c
& divide [# left, # right ] X #                   ~Function Declaration, return int~
<
    # quotient <- 0!                              ~Int assigment~
    O left <>> right                              ~While Loop [left => right]~
    <
        left <- left - right!                     ~Minus operator reassignment~
        quotient <- quotient + 1!                 ~Plus operator reassignment~
    >
    quotient -> !                                 ~Return Value~
>

& modulo [# left, # right ] X #                   ~Function Declaration, return int~
<
    # decrement <- right * divide[left, right]!   ~Multiply operator with function call~ 
    decrement <- left - decrement!                ~Minus operator reassignment~              
    decrement -> !                                ~Return Value~
>

& Main[] X #                                      ~Main Function Declaration~
<
    # num <- modulo[100, 21]!                     ~Function call assignment int~
    num -> !                                      ~Return value~
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

- Classes with inheritance ([astNode.py](./astNode.py))
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
      - lien 496, returnFile
  - zip
    - [interpreter.py](./interpreter.py)
      - line 563, ExecuteFunctionCallNode
      - line 566, ExecuteFunctionCallNode
- Multiple functions per file [exmaple](tests/modulo.arw)
- Calling functions within functions [example](tests/test-fibonachi.arw)


### Turing completeness

This language has a default flow of control, can store states, has conditional execution and repetition, which makes it able to execute/replicate the results of turing programs which makes it turing complete. 

