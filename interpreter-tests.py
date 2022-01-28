from KarkelLang import *
import inspect



testNr = 0
testSucceeded = 0

def eval_result():
    print(bcolors.OKBLUE + "Tests: " + str(testSucceeded) + "/" + str(testNr) + " Succeeded" + bcolors.RESET) 

def eval(functionName: str, expectedResult, output):
    
    global testNr
    global testSucceeded
    
    testNr = testNr + 1

    if(output.error == None):
        if(output.currentFunction.returnValue.value == expectedResult):
            testSucceeded = testSucceeded + 1
            print(bcolors.OKGREEN + functionName  + " Succeeded" + bcolors.RESET) 
        else:
            print(bcolors.FAIL + functionName  + " Failed, got: " + str(output.currentFunction.returnValue.value) + bcolors.RESET)
    else:
        print(bcolors.FAIL + functionName  + " Failed" + bcolors.RESET)
        print(bcolors.FAIL + output.error.what + bcolors.RESET)

def test_int():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int.arw"))

def test_int_operator_add_1():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-1.arw"))

def test_int_operator_add_2():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-2.arw"))
    
def test_int_operator_add_3():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-3.arw"))

def test_int_operator_add_4():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-add-4.arw"))

def test_int_reinit_operator_add_1():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-add-1.arw"))

def test_int_reinit_operator_add_2():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-add-2.arw"))

def test_int_reinit_operator_add_3():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-add-3.arw"))

def test_int_reinit_operator_sub_1():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-sub-1.arw"))

def test_int_reinit_operator_sub_2():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-sub-2.arw"))

def test_int_reinit_operator_sub_3():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit-operator-sub-3.arw"))

def test_int_operator_sub_1():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-sub-1.arw"))

def test_int_operator_sub_2():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-sub-2.arw"))

def test_int_operator_sub_3():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-int-operator-sub-3.arw"))

def test_int_reinit():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-init-reinit.arw"))

def test_string():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string.arw"))
  
def test_string_add_1():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-1.arw"))
  
def test_string_add_2():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-2.arw"))

def test_string_add_3():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-3.arw"))
 
def test_string_add_4():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-add-4.arw"))

def test_string_reinit():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-string-reinit.arw"))
    
def test_function_call_1():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-1.arw"))
    
def test_function_call_parameter_1():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-parameter-1.arw"))
    
def test_function_call_parameter_2():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-parameter-2.arw"))
    
def test_function_call_parameter_3():
    eval(inspect.currentframe().f_code.co_name, "Hi", run("tests/test-function-call-parameter-3.arw"))

def test_function_call_parameter_4():
    eval(inspect.currentframe().f_code.co_name, 10, run("tests/test-function-call-parameter-4.arw"))

if __name__ == "__main__":
    test_int()
    test_int_reinit();
    test_int_operator_add_1()
    test_int_operator_add_2()
    test_int_operator_add_3()
    test_int_operator_add_4()
    test_int_reinit_operator_add_1()
    test_int_reinit_operator_add_2()
    test_int_reinit_operator_add_3()
    test_int_operator_sub_1()
    test_int_operator_sub_2()
    test_int_operator_sub_3()
    test_string()
    test_string_reinit()
    test_string_add_1()
    test_string_add_2()
    test_string_add_3()
    test_string_add_4()
    test_function_call_1()
    test_function_call_parameter_1()
    test_function_call_parameter_2()
    test_function_call_parameter_3()
    test_function_call_parameter_4()
    eval_result()