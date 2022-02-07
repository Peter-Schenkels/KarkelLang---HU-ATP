from tokens import *
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def split(input : str) ->list:
    pattern = re.compile("(\s)")
    return pattern.sub('', input)

def countCharacterUntil(input : list, match: str, stop : str) -> int:
    if(input== []): 
        print("Character not in the list")
        return int("-inf")
    head, *tail = input
    if(head[0] == match): 
        return countCharacterUntil(tail, match, stop) + 1
    if(head[0] == stop): 
        return 0
    return countCharacterUntil(tail, match, stop);
    
def checkError(input : list, lineNr : int = 1):
    if(input == []):
        return 0
    head, *tail = input
    if(head.type == "Error"):
        return lineNr
    if(head.type == "NewLine"):
        lineNr += 1
    return checkError(tail, lineNr)
    
def AddLineNr(tokens, lineNr=1):
    if(tokens != []):
        head, *tail = tokens
        if(head.type == "NewLine"):
            lineNr += 1
            return AddLineNr(tail, lineNr)
        else:
            head.lineNr = lineNr
        return [head] + list(AddLineNr(tail, lineNr))
    return []
    
def lexer(input : str) -> list:
    patternInclusions = re.compile("(~|\d+|(?<={)(.*?)(?=})|\w+|O|@|->|<-|<>>|<<>|<<|>>|<>|<|>|\{|\}|!|\+|\-|\*|&|\[|\]|\?:|\?|:|#|,|\(|\)|\n)")
    mismatches = patternInclusions.sub('', (re.compile("\s").sub('', input)))
    if(len(mismatches) > 0):
        print(bcolors.FAIL + "Unknown Token [ " + mismatches[0] +  " ] at line: " + str(countCharacterUntil(split(input), "\n", mismatches[0]) + 1) + bcolors.RESET)
        return []
    tokens = AddLineNr(list(map(matchToken, patternInclusions.findall(input))))
    if(checkError(tokens) != 0):
        print("Invalid token at line: " + str(checkError(tokens)))
        return[]
    return tokens
