from tokens import *
class bcolors:
    """Class for printing colors in print functions
    """
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
    """Splits the input string into a list of tokens based on spaces

    Args:
        input (str): input string

    Returns:
        list: list of tokens
    """    
    pattern = re.compile("(\s)")
    return pattern.sub('', input)

def countCharacterUntil(input : list, match: str, stop : str) -> int:
    """Counts the number of characters until the match is found

    Args:
        input (list): list of tokens
        match (str): to be matched token
        stop (str): stop token

    Returns:
        int: number of characters
    """    
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
    """"Checks if the input list contains an error

    Args:
        input (list): input tokens
        lineNr (int, optional): current line Nr. Defaults to 1.

    Returns:
        _type_: _description_
    """
    if(input == []):
        return 0
    head, *tail = input
    if(head.type == "Error"):
        return lineNr
    if(head.type == "NewLine"):
        lineNr += 1
    return checkError(tail, lineNr)
    
def AddLineNr(tokens, lineNr=1):
    """Adds line numbers to the tokens
    Args:
        tokens (_type_): list of tokens
        lineNr (int, optional): current line Nr. Defaults to 1.

    Returns:
        _type_: _description_
    """    
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
    """Lexer for KarkelLang

    Args:
        input (str): ARW file to be lexed

    Returns:
        list: list of tokens to be parsed
    """    
    patternInclusions = re.compile("(~|(?<={)(.*?)(?=})|\d+|\w+|O|@|->|<-|<>>|<<>|<<|>>|<>|><|<|>|\{|\}|!|\+|\-|\*|&|\[|\]|\?:|\?|:|#|,|\(|\)|\n)")
    mismatches = patternInclusions.sub('', (re.compile("\s").sub('', input)))
    if(len(mismatches) > 0):
        print(bcolors.FAIL + "Unknown Token [ " + mismatches[0] +  " ] at line: " + str(countCharacterUntil(split(input), "\n", mismatches[0]) + 1) + bcolors.RESET)
        return []
    tokens = AddLineNr(list(map(matchToken, patternInclusions.findall(input))))
    if(checkError(tokens) != 0):
        print("Invalid token at line: " + str(checkError(tokens)))
        return[]
    return tokens
