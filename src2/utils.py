import heapdict as hd
import cartes_pac as plateau
import json
import numpy as np


def astar_generique(carte, pospac, posfantome):
    debut = tuple(posfantome)
    objectif = tuple(pospac)
    atraiter = hd.heapdict()
    atraiter[debut] = 0
    parents = {}
    d = {}
    parents[debut] = None
    d[debut] = 0
    while len(atraiter) > 0:
        x, _ = atraiter.popitem()
        posfantome = list(x)
        position = posfantome
        if x == objectif:
            break
        for coup in coup_possible(carte, posfantome):
            distance = d[x] + 1
            (x3, y3) = coup
            voisin = [position[0] + x3, position[1] + y3]
            clef = tuple(voisin)
            if clef not in d or distance < d[clef]:
                d[clef] = distance
                nouv_dist = distance + heuristique(voisin, list(objectif))
                atraiter[clef] = nouv_dist
                parents[clef] = x
    trajet = chemin(parents, debut, objectif)
    if len(trajet) > 1:
        return trajet[1]


def chemin(parents, debut, objectif):
    x = objectif
    path = [x]
    while x != debut:
        if x not in parents:
            return []
        x = parents[x]
        path.append(x)
    path.reverse()
    return path


def heuristique(posfantome, pospacman):
    x1, y1 = posfantome
    x2, y2 = pospacman
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def coup_possible(carte, position):
    mouvement = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    # haut,droite,bas,gauche
    res = []
    for mouv in mouvement:
        newpos = [position[0] + mouv[0], position[1] + mouv[1]]
        if (
            0 <= newpos[0] < len(carte)
            and 0 <= newpos[1] < len(carte[0])
            and carte[newpos[0]][newpos[1]] != "■"
        ):
            res.append(tuple(mouv))
    return res


def pos_possible(carte):
    res = []
    for i in range(len(carte)):
        for j in range(len(carte[i])):
            if carte[i][j] == " ":
                res.append((i, j))
    return res


if __name__ == "__main__":
    carte = plateau.map5["carte"]
    positions_possible = pos_possible(carte)
    n = len(positions_possible) ** 2
    c = 0
    coup_pour_fantomes = {}
    for fant in positions_possible:
        for pac in positions_possible:
            coup_pour_fantomes[
                f"{fant[0]},{fant[1]},{pac[0]},{pac[1]}"
            ] = astar_generique(carte, pac, fant)
            c += 1
            if c % 1000 == 0:
                print(f"{c}/{n}")

    with open("astar_pregen.txt", "w") as w:
        w.write(json.dumps(coup_pour_fantomes))
    print("done")
