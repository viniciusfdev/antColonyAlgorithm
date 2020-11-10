import pandas as pd
import numpy as np
import random
import typing
import copy 
import math
import sys

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return "\n|C => x: {}; y:{}|".format(self.x, self.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

def dist_two_pt(point_a: Point, point_b: Point) -> float:
    """Retorna a distancia euclidiana entre dois pontos"""
    return math.sqrt((point_a.x-point_b.x)**2 + (point_a.y-point_b.y)**2)

def load_colony(path: str):
    return pd.read_csv(r'%s' % path, ';').to_numpy()[:,1:]

def size_route(route: list, D: "matrix"):
    sum = 0
    for i in range(len(route)-1):
        sum += D[route[i]][route[i+1]]
    return sum

def make_probs(D: "matrix", gama_fer: "matrix", alpha: float, beta: float, i: int, route: list) -> list:
    # calculo da matriz de probabilidades
    prod_prob = [0 if D[i][j] == 0 or j in route else (gama_fer[i][j]**alpha) * (1/D[i][j])**beta
                for j in range(len(D[i]))]

    # calculo das probabilidades
    return [prod_prob[j] / sum(prod_prob)
            if i != j else 0
            for j in range(len(D))]

def definy_route(D: "matrix", gama_fer: "matrix", alpha: float, beta: float):

    # first random city
    i = round(random.uniform(0, len(D)-1))

    # rota inicial
    route = []
    route.append(i)

    while len(route) < len(D):
        probs = make_probs(D, gama_fer, alpha, beta, i, route)
        probs_wheel = []

        ss = 0
        for j, p in enumerate(probs):
            ss = ss + p
            probs_wheel.append(ss if p !=0 else 0)
        
        rand_value = random.uniform(0, probs_wheel[-1])

        for pos in range(len(probs_wheel)):
            if ((pos == 0 and rand_value < probs_wheel[pos]) or 
                rand_value >= probs_wheel[pos-1] and rand_value < probs_wheel[pos]):
                i = pos
                break

        route.append(i)

    return route

def aco(D: "matrix", sigma0: float, sigma: float, ro: float, alpha: float, beta: float) -> list:
    best = { "formiga": 0, "tam": sys.float_info.max, "numb_freq": 0, "route": [] }
    gama_fer = [[sigma0 for i in range(len(D))] for j in range(len(D))]

    routes = {}
    
    j = 0
    while best["numb_freq"] < 2*len(D) and j < 300:
        delta_fer = [[0 for i in range(len(D))] for j in range(len(D))]
        best_route = best["route"]
        for k in range(len(D)):
            # trace a rota
            routes[k] = definy_route(D, gama_fer, alpha, beta)

            # escolha do melhor
            lk = size_route(routes[k], D)

            if lk < best["tam"]:
                best["formiga"] = k
                best["tam"] = lk
                best["route"] = routes[k]

            # update feromonio delta
            delta_fer = [
                [delta_fer[j][i] + sigma/lk for i in range(len(D))] 
                for j in range(len(D))]

        if best["route"] == best_route:
            best["numb_freq"] = best["numb_freq"] + 1
        else:
            best["numb_freq"] = 1

        # update feromonio gama
        gama_fer = [
                [(1-ro) * gama_fer[i][j] + delta_fer[i][j] for i in range(len(D))] 
                for j in range(len(D))]
        
        j += 1

    return best

if __name__ == "__main__":
    colony = load_colony("colony.csv")
    colony = [Point(r[0], r[1]) for i, r in enumerate(colony)]
    m_adj = [[dist_two_pt(colony[i], colony[j]) for i in range(len(colony))] for j in range(len(colony))]


    print("Valor do feromônio inicial em cada arco: 0.02")
    print("Quantidade de feromônio de referência depositada nos arcos visitados: 0.3")
    print("Taxa de evaporação do feromônio a cada iteração: 0.1")
    print("Influência do feromônio no arco: alpha = beta = 1")
    print("\nRunning...")
    
    best = aco(m_adj, 0.02, 0.3, 0.1, 1, 1)

    print("Melhor obtido: ")
    print(best)