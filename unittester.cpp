#include <iostream>
#include <string>
#include <ostream>
#include <fstream>
#include <sstream>


// # check_call(['wsl', "arm-linux-gnueabi-as", "out.asm", "-o",  "out.o"])
// # check_call(['wsl', "arm-linux-gnueabi-gcc", "out.o", "-o",  "out.elf", "-nostdlib"])
// check_call(['wsl', "qemu-arm", "out.elf"])


namespace KarkelLang
{

    inline bool FileExists (const std::string& name) {
        std::ifstream file(name.c_str());
        return file.good();
    }

    inline bool isNumber(const std::string& input)
    {
        for (char const &character : input) {
            if (std::isdigit(character) == 0) return false;
        }
        return true;
    }

    inline int runTest(const std::string & input_file, const int & expected_result)
    {
        std::string run_arm_command = "qemu-arm " + input_file; 
        int result = system(run_arm_command.c_str()) >> 8;
        if(result == expected_result)
        {
            std::cout << "\033[92mTest succeeded! \033[1m\033[94m" << std::to_string(result) << "==" << std::to_string(expected_result) << "\033[0m" << std::endl;
        }
        else
        {
            std::cout << "\033[91mTest Failed, got: " << std::to_string(result) << ". Expected: " << std::to_string(expected_result) << "\033[0m" << std::endl;
        }
        return 0;
    }

    inline int StringToNumber(std::string & input)
    {
        int output = 0;
        std::stringstream convertor(input);
        convertor >> output;  
        return output;      
    }
}


int main (int argc, char *argv[])
{
    if(argc == 3)
    { 
        std::string src_elf = argv[1];
        std::string expected_result = argv[2];
        if(KarkelLang::isNumber(expected_result))
        {
            if(KarkelLang::FileExists(src_elf))
            {
                return KarkelLang::runTest(src_elf, KarkelLang::StringToNumber(expected_result));
            }
            else
            {
                std::cout << "File doesn't exist" << std::endl;
            }
        }
        else
        {
            std::cout << "Expected a number" << std::endl;
        }
    }
    else
    {
        std::cout << "Expected 2 Arguments not: " << std::to_string(argc) << std::endl;
    }
}