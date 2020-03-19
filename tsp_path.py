import ast
import matplotlib.pyplot as plt


if __name__ == '__main__':

    cities = []

    with open('eil51.tsp', 'r') as f:
        while True:
            line = f.readline()
            if line == 'EOF' or not line:
                break
            else:
                arr = line.split(' ')
                if arr[0].isnumeric():
                    # 新增城市 索引調整為由0開始
                    cities.append((int(arr[1]), int(arr[2])))

    path = ast.literal_eval(input('Enter path array string:'))
    fig = plt.figure(figsize=(6, 5))
    sub_best = fig.add_subplot(111)
    sub_best.axis([0, 70, 0, 80])
    for c in range(len(cities)):
        sub_best.scatter(cities[c][0], cities[c][1])
        sub_best.annotate(str(c), cities[c])
    for p in range(len(path) - 1):
        sub_best.plot([cities[path[p]][0], cities[path[p + 1]][0]], [cities[path[p]][1], cities[path[p + 1]][1]], 'red')
                    
    plt.show()
