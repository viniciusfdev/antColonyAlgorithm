import pandas as pd
import numpy as np
import typing
import math
import sys

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return "\n|C => x: {}; y:{}|".format(self.x, self.y)

def dist_two_pt(point_a: Point, point_b: Point) -> float:
    """
    Retorna a distancia euclidiana entre dois pontos
    """
    return math.sqrt((point_a.x-point_b.x)**2 + (point_a.y-point_b.y)**2)

def load_colony(path: str):
    return pd.read_csv(r'%s' % path, ';').to_numpy()[:,1:]

def size_route(route: list):
    sum = 0
    for i in range(len(route)-1):
        sum += dist_two_pt(route[i], route[i+1])
    return sum

def definy_route(D: matrix, teta: matrix, alpha: float, beta: float):
    pass

def aco(D: matrix, sigma0: float, sigma: float, ro: float, alpha: float, beta: float):
    best = { "i": 0, "tam": sys.float_info.max, "n": 0 }
    teta = [[sigma0 for i in range(len(colony))] for j in range(len(colony))]
    
    while best["n"] < len(D):
        for k in range(len(D)): # para cada formiga k
            route_k = definy_route(D, teta, alpha, beta)
            if size_route(route_k) < best["tam"]:
                best["i"] = k
                best["tam"] = size_route(route_k)
                best["n"] = 0
            else:
                best["n"] = best["n"] + 1

if __name__ == "__main__":
    print("Start...")
    colony = load_colony("colony.csv")
    colony = [Point(r[0], r[1]) for i, r in enumerate(colony)]
    m_adj = [[dist_two_pt(colony[i], colony[j]) for i in range(len(colony))] for j in range(len(colony))]


    aco(m_adj, 0, 0.1, 0.5, 0.1, 0.1)