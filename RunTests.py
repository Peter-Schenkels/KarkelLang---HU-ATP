from KarkelLang import *
import inspect

sys.setrecursionlimit(3000)

testNr = 0
testSucceeded = 0

def eval_result():
    print(bcolors.OKBLUE + "Tests: " + str(testSucceeded) + "/" + str(testNr) + " Succeeded" + bcolors.RESET) 

def eval(functionName: str, expectedResult, output):

    global testNr
    global testSucceeded
    
    testNr = testNr + 1
    if(hasattr(output, "currentFunction")):
        if(output):
            if(output.error == None):
                if(output.currentFunction.returnValue.value == expectedResult):
                    testSucceeded = testSucceeded + 1
                    print(bcolors.OKGREEN + functionName  + " Succeeded" + bcolors.RESET) 
                else:
                    print(bcolors.FAIL + functionName  + " Failed, got: " + str(output.currentFunction.returnValue.value) + bcolors.RESET)
            else:
                print(bcolors.FAIL + functionName  + " Failed, " + output.error.what + bcolors.RESET)
        else:
            print(bcolors.FAIL + functionName  + " Failed")
    else:
        if(output == expectedResult):
                testSucceeded = testSucceeded + 1
                print(bcolors.OKGREEN + functionName  + " Succeeded" + bcolors.RESET) 
        else:
            print(bcolors.FAIL + functionName  + " Failed, got: " + str(output) + bcolors.RESET)

def test_int(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_operator_add_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-1.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_int_operator_multiply_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-multiply-1.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_operator_add_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-2.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_int_operator_add_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-3.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_operator_add_4(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-4.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_int_operator_add_5(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-5.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_reinit_operator_add_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-add-1.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_reinit_operator_add_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-add-2.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_reinit_operator_add_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-add-3.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_reinit_operator_sub_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-sub-1.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_reinit_operator_sub_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-sub-2.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_reinit_operator_sub_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-sub-3.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_operator_sub_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-sub-1.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_operator_sub_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-sub-2.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_operator_sub_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-sub-3.arw", compile, inspect.currentframe().f_code.co_name))

def test_int_reinit(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit.arw", compile, inspect.currentframe().f_code.co_name))

def test_string(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string.arw", compile, inspect.currentframe().f_code.co_name))
  
def test_string_add_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-1.arw", compile, inspect.currentframe().f_code.co_name))
  
def test_string_add_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-2.arw", compile, inspect.currentframe().f_code.co_name))

def test_string_add_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-3.arw", compile, inspect.currentframe().f_code.co_name))
 
def test_string_add_4(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-4.arw", compile, inspect.currentframe().f_code.co_name))

def test_string_reinit(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-reinit.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_function_call_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-1.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_function_call_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 3, run("tests/test-function-call-2.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_function_call_parameter_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-parameter-1.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_function_call_parameter_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-parameter-2.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_function_call_parameter_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-parameter-3.arw", compile, inspect.currentframe().f_code.co_name))

def test_function_call_parameter_4(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-function-call-parameter-4.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_function_call_parameter_5(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-function-call-parameter-5.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_if_statement_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-if-statement-1.arw", compile, inspect.currentframe().f_code.co_name))

def test_if_statement_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, "aaaaaaaaaa", run("tests/test-if-statement-2.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_if_statement_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-if-statement-3.arw", compile, inspect.currentframe().f_code.co_name))

def test_fibonachi(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 55 , run("tests/test-fibonachi.arw", compile, inspect.currentframe().f_code.co_name))

def test_fibonachi_compiler(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 55 , run("tests/test-fibonachi-compiler.arw", compile, inspect.currentframe().f_code.co_name))

def test_array_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10 , run("tests/test-array-1.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_while_loop_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10 , run("tests/test-while-loop-1.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_while_loop_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10 , run("tests/test-while-loop-2.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_print_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 0 , run("tests/test-print-1.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_print_2(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 0 , run("tests/test-print-2.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_print_3(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 0 , run("tests/test-print-3.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_function_call_parameter_array(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10 , run("tests/test-function-call-parameter-array.arw", compile, inspect.currentframe().f_code.co_name))

def division_test(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 10 , run("tests/division-test.arw", compile, inspect.currentframe().f_code.co_name))

def test_char_1(compile:bool):
    eval(inspect.currentframe().f_code.co_name, ord('a') , run("tests/test-char.arw", compile, inspect.currentframe().f_code.co_name))
    
def test_char_print(compile:bool):
    eval(inspect.currentframe().f_code.co_name, ord('a') , run("tests/test-print-char.arw", compile, inspect.currentframe().f_code.co_name))
    
def print_number(compile:bool):
    eval(inspect.currentframe().f_code.co_name, ord('a') , run("tests/print-number.arw", compile, inspect.currentframe().f_code.co_name))

def modulo_test(compile:bool):
    eval(inspect.currentframe().f_code.co_name, 16 , run("tests/modulo.arw", compile, inspect.currentframe().f_code.co_name))
    
    
if __name__ == "__main__":
    compile = True
    test_int(compile)
    test_int_reinit(compile)
    test_int_operator_add_1(compile)
    test_int_operator_add_2(compile)
    test_int_operator_add_3(compile)
    test_int_operator_add_4(compile)
    test_int_reinit_operator_add_1(compile)
    test_int_reinit_operator_add_2(compile)
    test_int_reinit_operator_add_3(compile)
    test_int_operator_multiply_1(compile)
    test_int_operator_sub_1(compile)
    test_int_operator_sub_2(compile)
    test_int_operator_sub_3(compile)
    if(compile is not True):
        test_string(False)
        test_string_reinit(False)
        test_string_add_1(False)
        test_string_add_2(False)
        test_string_add_3(False)
        test_string_add_4(False)
        test_function_call_1(False)
    test_function_call_2(compile)
    if(compile is not True):  
        test_function_call_parameter_1(False)
        test_function_call_parameter_2(False)
        test_function_call_parameter_3(False)
    test_function_call_parameter_4(compile)
    test_function_call_parameter_5(compile)
    test_if_statement_1(compile)
    if(compile is not True):  
        test_if_statement_2(False)
    test_if_statement_3(compile)
    test_fibonachi(compile)
    if(compile is not True):
        test_array_1(False)
    test_while_loop_1(compile)
    test_while_loop_2(compile)
    test_print_1(compile)
    test_print_2(compile)
    test_print_3(compile)
    if(compile is True):
        test_char_1(compile)
        test_char_print(compile)
    division_test(compile)
    modulo_test(compile)
    eval_result()