import random as random

class myClass:

    
    def __init__(self, lengthOfList):
        self.myRandomList = []
        for i in range(0,lengthOfList):
            self.myRandomList.append(random.uniform(-1.0,1.0))

a = myClass(2)
b = myClass(1)

print(a.myRandomList)
print(b.myRandomList)