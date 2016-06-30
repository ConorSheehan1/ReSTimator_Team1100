'''
Basic shuffle to decide what order we present in
'''

import random
mylist = ["andy", "conor", "john", "stephen"]

answer = random.shuffle(mylist)
if __name__ == "__main__":
    print(mylist)

result = ['andy', 'stephen', 'john', 'conor']
