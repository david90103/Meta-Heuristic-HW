import math
import random
import matplotlib.pyplot as plt
from datetime import datetime


class City:

    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def __str__(self):
        return 'City' + str(self.index) + ' at (' + str(self.x) + ', ' + str(self.y) + ')'
    
    def distance(self, target):
        return math.sqrt(((self.x - target.x)**2)+((self.y - target.y)**2))

class Ant:

    def __init__(self):
        self.path = []
        self.score = 0
        self.total_distance = 0

class ACO:
    
    def __init__(self, ants_size, alpha, beta, evaporation):
        self.cities = []
        self.alpha = alpha              # 費洛蒙指數參數
        self.beta = beta                # 距離指數參數
        self.evaporation = evaporation  # 蒸發係數
        self.ants = []
        self.ants_size = ants_size
        self.q = 100
        self.pheromone = []             # 費洛蒙表
        self.distance = []              # 城市距離表
        self.best = 999999
        self.bestpath = []
        self.generation_best = 999999
        self.generation_best_path = []
        
    def initialize(self):
        ''' Initialize pheromone table and distance table'''
        self.distance = []
        self.pheromone = []
        for i in range(len(self.cities)):
            self.pheromone.append([0.01 for j in range(len(self.cities))])
        for i in range(len(self.cities)):
            self.distance.append([])
            for j in range(len(self.cities)):
                self.distance[i].append(self.cities[i].distance(self.cities[j]))

    def add_city(self, city):
        self.cities.append(city)
    
    def roulette_wheel(self, current_city, cities):
        total = 0.0
        temp = []
        normalized_array = []
        for c in cities:
            result = (self.pheromone[current_city][c] ** self.alpha) * ((1 / self.distance[current_city][c]) ** self.beta)
            temp.append(result)
            total += result
        
        # return random city if total is 0
        if total == 0:
            return random.choice(cities)

        for c in range(len(cities)):
            normalized_array.append(temp[c] / total)
        
        return random.choices(cities, normalized_array)[0]

    def make_ants(self):
        self.ants = []
        for i in range(self.ants_size):
            ant = Ant()
            ant.path.append(0) # start point

            for j in range(len(self.cities) - 1):
                not_been_cities = []
                for city in self.cities:
                    if city.index not in ant.path:
                        not_been_cities.append(city.index)
                ant.path.append(self.roulette_wheel(ant.path[-1], not_been_cities))

            ant.path.append(0) # end point

            # local search
            if random.random() < 0.8:
                start_point = random.randint(1, len(self.cities) - 3 - 1)
                temp = ant.path[start_point]
                ant.path[start_point] = ant.path[start_point + 3]
                ant.path[start_point + 3] = temp
                temp = ant.path[start_point + 1]
                ant.path[start_point + 1] = ant.path[start_point + 2]
                ant.path[start_point + 2] = temp
                # start_point = random.randint(1, len(self.cities) - 4 - 1)
                # temp = ant.path[start_point: start_point + 4]
                # random.shuffle(temp)
                # ant.path[start_point:start_point + 4] = temp
            
            # random switch
            # if random.random() < 0.5:
            #     a = random.randint(1, len(self.cities) - 1)
            #     b = random.randint(1, len(self.cities) - 1)
            #     temp = ant.path[a]
            #     ant.path[a] = ant.path[b]
            #     ant.path[b] = temp
                
            self.ants.append(ant)

    def run_ants(self):
        self.generation_best = 999999
        for ant in self.ants:
            for i in range(len(ant.path) - 1):
                distance = self.distance[ant.path[i]][ant.path[i + 1]]
                if distance > 20:
                    ant.score += distance * 10
                else: 
                    ant.score += distance
                ant.total_distance += distance
            if ant.total_distance < self.generation_best:
                self.generation_best = ant.total_distance
                self.generation_best_path = ant.path
            if ant.total_distance < self.best:
                self.best = ant.total_distance
                self.bestpath = ant.path

    def update_pheromone(self):
        pheromone_effects = [] # array of [c_from, c_to, value]
        for ant in self.ants:
            for i in range(len(ant.path) - 1):
                pheromone_effects.append([ant.path[i], ant.path[i + 1], self.q / ant.score])
        for i in range(len(self.pheromone)):
            for j in range(len(self.pheromone)):
                self.pheromone[i][j] *= self.evaporation
        for elem in pheromone_effects:
            self.pheromone[elem[0]][elem[1]] += elem[2]

    def next_generation(self):
        self.make_ants()
        self.run_ants()
        self.update_pheromone()


if __name__ == '__main__':

    show_graph = True
    log_to_file = False
    best = 99999
    # params = {
    #     'ants': [10, 20, 100],
    #     'a': [1, 1.5],
    #     'b': [2, 3, 3.5],
    #     'evaporation': [0.6, 0.7, 0.8, 0.9]
    # }

    while True:

        # aco = ACO(params['ants'][random.randint(0, 2)], params['a'][random.randint(0, 1)], params['b'][random.randint(0, 2)], params['evaporation'][random.randint(0, 3)])
        aco = ACO(20, 1, 4, 0.9)

        with open('eil51.tsp', 'r') as f:
            while True:
                line = f.readline()
                if line == 'EOF' or not line:
                    break
                else:
                    arr = line.split(' ')
                    if arr[0].isnumeric():
                        # 新增城市 索引調整為由0開始
                        aco.add_city(City(int(arr[0]) - 1, int(arr[1]), int(arr[2])))
    
        # draw result
        if show_graph:
            plt.ion()
            fig = plt.figure(figsize=(13, 13))
            sub_best = fig.add_subplot(221)
            sub_best.axis([0, 70, 0, 80])
            sub_pheromone = fig.add_subplot(223)
            sub_pheromone.axis([0, 70, 0, 80])
            sub_gen_best = fig.add_subplot(224)
            sub_gen_best.axis([0, 70, 0, 80])
            sub_result = fig.add_subplot(222)


        # run algorithm
        aco.initialize()
        results = []
        for i in range(1000000):
            aco.next_generation()
            results.append(aco.generation_best)
            if i % 200 == 0:
                if aco.best < best and log_to_file:
                    best = aco.best
                    with open('aco_results.txt', 'a') as f:
                        line = datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + 'ants:10 alpha:1 beta:3 evaporation:0.9 iteration:300 RESULT: ' + str(round(aco.best, 2)) + ' PATH: ' + str(aco.bestpath) + '\n'
                        f.write(line)
                # clear pheromone
                aco.initialize()
                results = []
            if (i+1) % 100 == 0:
                print(round(aco.best, 2), round(aco.generation_best, 2), 'GEN', str(i + 1))
                if show_graph:
                    sub_best.cla()
                    sub_pheromone.cla()
                    sub_gen_best.cla()
                    sub_result.cla()
                    # draw cities
                    for c in aco.cities:
                        sub_best.scatter(c.x, c.y)
                        sub_best.annotate(str(c.index), (c.x, c.y))
                        sub_pheromone.scatter(c.x, c.y)
                        sub_pheromone.annotate(str(c.index), (c.x, c.y))
                        sub_gen_best.annotate(str(c.index), (c.x, c.y))
                        sub_gen_best.scatter(c.x, c.y)
                    # draw  path
                    for i in range(len(aco.generation_best_path) - 1):
                        # best path
                        x1, x2 = aco.cities[aco.bestpath[i]].x, aco.cities[aco.bestpath[i + 1]].x
                        y1, y2 = aco.cities[aco.bestpath[i]].y, aco.cities[aco.bestpath[i + 1]].y
                        sub_best.plot([x1, x2], [y1, y2], 'red')
                        # generation best
                        x1, x2 = aco.cities[aco.generation_best_path[i]].x, aco.cities[aco.generation_best_path[i + 1]].x
                        y1, y2 = aco.cities[aco.generation_best_path[i]].y, aco.cities[aco.generation_best_path[i + 1]].y
                        sub_gen_best.plot([x1, x2], [y1, y2], 'orange')
                    # draw results
                    sub_result.plot(results)
                    # draw pheromone 
                    total_pheromone = 0
                    for i in range(len(aco.cities)):
                        for j in range(len(aco.cities)):
                            total_pheromone += aco.pheromone[aco.cities[i].index][aco.cities[j].index]
                            
                    normalized_pheromone = []
                    for i in range(len(aco.cities)):
                        normalized_pheromone.append([])
                        for j in range(len(aco.cities)):
                            normalized_pheromone[i].append(aco.pheromone[aco.cities[i].index][aco.cities[j].index] / total_pheromone)
                    
                    for i in range(len(aco.cities)):
                        for j in range(len(aco.cities)):
                            x1, x2 = aco.cities[i].x, aco.cities[j].x
                            y1, y2 = aco.cities[i].y, aco.cities[j].y
                            sub_pheromone.plot([x1, x2], [y1, y2], 'blue', alpha=40 * normalized_pheromone[i][j])
                    
                    fig.canvas.draw()
                    fig.canvas.flush_events()

        if show_graph:
            plt.ioff()
            plt.show()

        # if log_to_file:
        #     with open('aco_results.txt', 'a') as f:
        #         line = datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + 'ants:' + str(aco.ants_size) + ' alpha:' + str(aco.alpha) + ' beta:' + str(aco.beta) + ' evaporation:' + str(aco.evaporation) + ' iteration:1000 RESULT: ' + str(round(aco.best, 2)) + ' PATH: ' + str(aco.bestpath) + '\n'
        #         f.write(line)
        #         print(line)
