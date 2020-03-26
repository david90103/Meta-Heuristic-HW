import random

def evaluate(arr):
    s = 0
    for elem in arr:
        if elem == 1:
            s += 1
    return s

#init
current = []
best = []
for i in range(50):
    current.append(random.randint(0, 1))

best_eval = 0
i = 0
while True:
    current = []
    for j in range(50):
        current.append(random.randint(0, 1))
    e = evaluate(current)
    if e > best_eval:
        best = current
        best_eval = e
    if i % 100000 == 0:
        print(i, best, best_eval)
    i += 1

    