import numpy as np
import matplotlib.pyplot as plt

import time


class DNA:
    def __init__(self, value, fitness):
        self.value = value
        self.fitness = fitness

    def __str__(self):
        return str(self.value) + ' Fitness: ' + str(self.fitness)


class GA:
    def __init__(self, dna_size,  pop_size, crossover_rate, mutation_rate):
        self.dna_size = dna_size
        self.population_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.normalized_fitness_array = []

    def initialize(self):
        for i in range(self.population_size):
            dna_value = np.random.randint(2, size=self.dna_size)
            dna_fitness = self.evaluate(dna_value)
            self.population.append(DNA(dna_value, dna_fitness))

        self.order()

    def order(self):
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        fitness_array = list(o.fitness for o in self.population)
        self.normalized_fitness_array = [
            float(i) / sum(fitness_array) for i in fitness_array]

    def best(self):
        return self.population[0]

    def evaluate(self, dna):
        return np.sum(dna)

    def crossover(self):
        # TODO Roulette wheel SLOW
        father = np.random.choice(
            self.population, p=self.normalized_fitness_array)
        mother = np.random.choice(
            self.population, p=self.normalized_fitness_array)

        index = np.random.randint(self.dna_size)
        new_dna = np.concatenate((father.value[:index], mother.value[index:]))
        return DNA(new_dna, self.evaluate(new_dna))

    def mutation(self, dna):
        index = np.random.randint(self.dna_size)
        dna.value[index] = (dna.value[index] + 1) % 2
        return dna

    def evolution(self):
        for i in range(round(self.population_size * self.crossover_rate)):
            # crossover
            new_dna = self.crossover()
            # mutation
            if np.random.random() < self.mutation_rate:
                new_dna = self.mutation(new_dna)

            self.population.pop()
            self.population.insert(0, new_dna)

        self.order()


if __name__ == '__main__':

    ga1 = GA(200, 100, 0.8, 0.3)
    ga1.initialize()

    ga2 = GA(200, 100, 0.8, 0.03)
    ga2.initialize()

    ga3 = GA(200, 100, 0.8, 0)
    ga3.initialize()

    fitness = [[], [], []]

    for generation in range(500):
        ga1.evolution()
        ga2.evolution()
        ga3.evolution()
        fitness[0].append(ga1.best().fitness)
        fitness[1].append(ga2.best().fitness)
        fitness[2].append(ga3.best().fitness)
        print(ga1.best().fitness, ga2.best().fitness,
              ga3.best().fitness, 'Gen', generation)

    # draw result
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.plot(fitness[0], label='GA1')
    plt.plot(fitness[1], label='GA2')
    plt.plot(fitness[2], label='GA3')
    plt.legend(loc='lower right')
    plt.show()
