from random import randint

n = []

rand_number = randint(0, 1000)

if rand_number >= 500:
    print(f'Number: {rand_number}')
else:
    n.append(rand_number)
    print(f' data list of number: {n}')

