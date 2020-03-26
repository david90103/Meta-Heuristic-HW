import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


class Particle:

    def __init__(self, x, v, p_best, p_best_value):
        self.x = x
        self.v = v
        self.p_best = p_best
        self.p_best_value = p_best_value
        self.path = []

class Pso:

    def __init__(self, p_size, w, c1, c2):
        self.c1 = c1
        self.c2 = c2
        self.w = w
        self.g_best_value = 999999
        self.g_best = np.empty((2, 1))
        self.particles = []
        for i in range(p_size):
            x = np.random.uniform(low=-40, high=40, size=(2, 1))
            v = np.zeros((2, 1))
            p_best_value = self.ackley(x)
            self.particles.append(Particle(x, v, x, p_best_value))
            if p_best_value < self.g_best_value:
                self.g_best_value = p_best_value
                self.g_best = x

    def ackley(self, x1, x2 = None):
        if x2:
            x = np.array([x1, x2])
        else:
            x = x1
        d = 2

        exp1 = np.exp((-0.2) * np.sqrt(np.sum(x**2) / d))
        exp2 = np.exp(np.sum(np.cos(2 * np.pi * x)) / d)

        return -20 * exp1 - exp2 + 20 + np.exp(1)

    def next_iteration(self):
        for p in self.particles:
            p.v = self.w * p.v + np.random.rand(2, 1) * self.c1 * (p.p_best - p.x) + np.random.rand(2, 1) * self.c2 * (self.g_best - p.x)
            p.x += p.v
            value = self.ackley(p.x)
            if value < p.p_best_value:
                p.p_best = p.x
                p.p_best_value = value
            if value < self.g_best_value:
                self.g_best_value = value
                self.g_best = p.x
                print(value)


if __name__ == '__main__':
    pso = Pso(100, 0.5, 0.2, 0.2)

    X1 = np.arange(-40, 40, 0.25)
    X2 = np.arange(-40, 40, 0.25)
    Z = np.empty((len(X1), len(X2)))
    X1, X2 = np.meshgrid(X1, X2)

    for i in range(3):
        pso.next_iteration()

    fig = plt.figure(figsize=(14, 5))
    
    ax = fig.add_subplot(121, projection='3d')
    bx = fig.add_subplot(122)

    for i in range(len(X1)):
        for j in range(len(X2)):
            Z[i][j] = pso.ackley(X1[i][j], X2[i][j])
        
    ax.plot_surface(X1, X2, Z, cmap=cm.coolwarm, antialiased=False, alpha=0.3)

    for p in pso.particles:
        ax.scatter(p.x[0], p.x[1], pso.ackley(p.x))

    fig.show()
    input()