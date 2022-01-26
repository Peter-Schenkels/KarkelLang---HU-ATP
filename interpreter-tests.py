from KarkelLang import *
import inspect


def test_int():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int.arw")
    if(output.error == None):
        if(output.currentFunction.returnValue.value == 10):
            print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
        else:
            print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
        print(bcolors.FAIL + output.error.what + bcolors.RESET)
    return output   

def test_int_operator_add_1():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int-operator-add-1.arw")
    if(output.error == None):
        if(output.currentFunction.returnValue.value == 10):
            print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
        else:
            print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_operator_add_2():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int-operator-add-2.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   
    
def test_int_operator_add_3():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int-operator-add-3.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output     

def test_int_operator_add_4():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int-operator-add-4.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output     

def test_int_reinit_operator_add_1():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-init-reinit-operator-add-1.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_reinit_operator_add_2():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-init-reinit-operator-add-2.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_reinit_operator_add_3():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-init-reinit-operator-add-3.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_reinit_operator_sub_1():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-init-reinit-operator-sub-1.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_reinit_operator_sub_2():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-init-reinit-operator-sub-2.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_reinit_operator_sub_3():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-init-reinit-operator-sub-3.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_operator_sub_1():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int-operator-sub-1.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_operator_sub_2():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int-operator-sub-2.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_operator_sub_3():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-int-operator-sub-3.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_int_reinit():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-init-reinit.arw")
    if(output.currentFunction.returnValue.value == 10):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_string():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-string.arw")
    if(output.currentFunction.returnValue.value == "Hi"):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output 
  
def test_string_add_1():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-string-add-1.arw")
    if(output.currentFunction.returnValue.value == "Hi"):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output 
  
def test_string_add_2():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-string-add-2.arw")
    if(output.currentFunction.returnValue.value == "Hi"):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   

def test_string_add_3():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-string-add-3.arw")
    if(output.currentFunction.returnValue.value == "Hi"):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output  
 
def test_string_add_4():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-string-add-4.arw")
    if(output.currentFunction.returnValue.value == "Hi"):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   


def test_string_reinit():
    this_function_name = inspect.currentframe().f_code.co_name
    output = run("tests/test-string-reinit.arw")
    if(output.currentFunction.returnValue.value == "Hi"):
        print(bcolors.OKGREEN + this_function_name  + " Succeeded" + bcolors.RESET) 
    else:
        print(bcolors.FAIL + this_function_name  + " Failed" + bcolors.RESET)
    return output   


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
    # test_int_reinit_operator_sub_1()
    # test_int_reinit_operator_sub_2()
    # test_int_reinit_operator_sub_3()