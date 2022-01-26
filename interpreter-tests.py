from KarkelLang import *
import inspect

def eval(functionName: str, expectedResult, output):
    if(output.error == None):
        if(output.currentFunction.returnValue.value == expectedResult):
            print(bcolors.OKGREEN + functionName  + " Succeeded" + bcolors.RESET) 
        else:
            print(bcolors.FAIL + functionName  + " Failed" + bcolors.RESET)
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