import re


if __name__ == '__main__':
    pattern = re.compile("\w+|^[A-Za-z]+$|\s+")
    print(pattern.findall("Arkel Arkel1"))
    print(pattern.match("Arkel1"))