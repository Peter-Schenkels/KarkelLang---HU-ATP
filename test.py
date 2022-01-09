import re
import json
import jsonpickle


class karkel():
    def __init__(self, number):
        self.number = number
        self.urkel = []
    def __str__(self):
        serialized = jsonpickle.encode(self)
        return json.dumps(json.loads(serialized), indent=2)
    


if __name__ == '__main__':
    jerkel = karkel(0)
    jerkel.urkel.append(12)
    circkel  = jerkel.urkel[0]
    circkel = 1
    for i in jerkel.urkel:
        print(i)