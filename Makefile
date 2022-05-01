BIN=./bin
TESTNAME=modulo
EXPECTED_RESULT=16
FALSE_RESULT=17

clean: 
	@rm -rf $(BIN)

build: 
	@mkdir -p $(BIN)
	@python3.10 ./KarkelLang.py tests/$(TESTNAME).arw --compile .$(BIN)/$(TESTNAME) 
	arm-linux-gnueabi-as $(BIN)/$(TESTNAME).asm -o $(BIN)/$(TESTNAME).o
	arm-linux-gnueabi-gcc $(BIN)/$(TESTNAME).o -o  $(BIN)/$(TESTNAME).elf -nostdlib
	g++ unittester.cpp -o $(BIN)/unittester

run: build
	@$(BIN)/unittester $(BIN)/$(TESTNAME).elf $(EXPECTED_RESULT)
	@$(BIN)/unittester $(BIN)/$(TESTNAME).elf $(FALSE_RESULT)

