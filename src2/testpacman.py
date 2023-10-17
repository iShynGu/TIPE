import copy
import time
import numpy as np
import heapdict as hd
import cartes_pac as cartes
import random

Niveau = dict


class Node:
    def __init__(self, move, plateau):
        self.move = move
        self.win = 0
        self.visits = 0
        self.children = {}
        # clef=coup, valeur=node
        self.est_terminal = False
        self.plateau = plateau

    def est_feuille(self):
        if self.plateau.victoire() or self.plateau.vie_en_moins():
            return True
        return False

    def selection(self):
        if self.est_feuille():
            return self
        if len(self.children) == 0:
            return self
        return self.uct()

    def expansion(self, carte1):
        if self.est_feuille():
            return 0
        plateau = self.plateau
        coups = plateau.coup_possible_pacman(carte1)
        if len(self.children) != len(coups):
            for coup in coups:
                if coup not in self.children:
                    plateau1 = plateau.copy()
                    plateau1.joue(carte1, coup)
                    noeud = Node(coup, plateau1)
                    resultat = rollout(noeud.plateau, carte1)
                    noeud.update(resultat)
                    self.children[coup] = noeud

    def update(self, resultat):
        self.visits += 1
        self.win += resultat

    @staticmethod
    def aux_uct(wi, ni, Ni):
        if Ni == 0:
            return 0
        else:
            return wi / ni + np.sqrt(2) * np.sqrt(np.log(Ni) / ni)

    def uct(self):
        Ni = self.visits
        maxi = -float("inf")
        res = None
        for coup in self.children:
            ni = self.children[coup].visits
            wi = self.children[coup].win
            if self.aux_uct(wi, ni, Ni) > maxi:
                maxi = self.aux_uct(wi, ni, Ni)
                res = coup
        return res


def rollout(plateau, carte):
    plateau1 = copy.deepcopy(plateau)
    compteur = 0
    while not plateau1.vie_en_moins() or plateau1.victoire():
        coups = plateau1.coup_possible(carte)
        (i, j) = random.choice(coups)
        plateau1.joue(carte, (i, j))
        compteur += 1
    if plateau1.victoire() or compteur >= 6:
        return 1
    else:
        return 0


def MCTS1(niveau):
    plateau = Board(niveau)
    root_node = Node(None, plateau)
    compteur = 0
    while not plateau.vie_en_moins() and compteur < 5:
        n, s = root_node, copy.deepcopy(etat)
        n.expansion(state)
        compteur2 = 0
        while not n.est_feuille(state) and compteur2 < 5:
            n = n.selection(state)
            # jouer le coup
            mouv = n.move
            i, j = mouv
            k, l = astar_for_ghost(s)
            deplace(s, "pacman", i, j)
            s["f"] = [k, l]
            deplace(s, "f", k, l)
            mange_fruit(s)
            # jouer le coup
            n.expansion(s)
            compteur2 += 1
        n = n.selection(state)
        print(1)
        resultat = rollout(s)
        while n.a_parent():
            n.updtate(resultat)
            n = n.parent
            print(2)
        compteur += 1
    return n.parent


class Board:
    def __init__(self, niveau):
        self.fruits = niveau["fruits"].copy()
        self.pospacman = niveau["pac"].copy()
        self.posfantomes = niveau["ghost"].copy()
        self.nombre_vies = 3
        self.score = 0

    def affiche_board(self, niveau):
        board = self.board_avec_persos(niveau["carte"])
        for line in board:
            for x in line:
                print(x, end="")
            print()

    def board_avec_persos(self, niveau):
        board = copy.deepcopy(niveau)
        for u in range(len(self.fruits)):
            i, j = self.fruits[u]
            ligne = list(board[i])
            ligne[j] = "•"
            board[i] = "".join(ligne)
        i0, j0 = self.pospacman
        ligne = list(board[i0])
        ligne[j0] = "ᗧ"
        board[i0] = "".join(ligne)
        for k in range(len(self.posfantomes)):
            i, j = self.posfantomes[k]
            ligne = list(board[i])
            print(self.posfantomes[k])
            ligne[j] = "ᗣ"
            board[i] = "".join(ligne)

        return board

    def deplace_pacman(self, i, j):
        position = self.pospacman
        self.pospacman = [position[0] + i, position[1] + j]

    def deplace_fantome(self, k, i, j):
        self.posfantomes[k] = [i, j]

    def vie_en_moins(self):
        for k in range(3):
            if self.pospacman == self.posfantomes[k]:
                return True
        return False

    def reset_map(self, i):
        print("Une vie en moins")
        self.nombre_vies = 3 - i
        print("nombre de vies =", self.nombre_vies)
        time.sleep(1)

    def fin_partie(self):
        if self.nombre_vies == 0:
            return True
        return False

    def coup_possible(self, carte):
        position = self.pospacman
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

    def coup_possible_fantome(self, carte: list[str], k: int):
        position = self.posfantomes[k]
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

    @staticmethod
    def heuristique(posfantome, pospacman):
        x1, y1 = posfantome
        x2, y2 = pospacman
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def is_close(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) < 5

    def astar_for_ghost(self, k, carte):
        [x2, y2] = random.choice(self.coup_possible_fantome(carte, k))
        debut = tuple(self.posfantomes[k])
        a1, b1 = debut
        objectif = tuple(self.pospacman)
        atraiter = hd.heapdict()
        atraiter[debut] = 0
        parents = {}
        d = {}
        parents[debut] = None
        d[debut] = 0
        while len(atraiter) > 0:
            x, _ = atraiter.popitem()
            self.posfantomes[k] = list(x)
            position = self.posfantomes[k]
            if x == objectif:
                break
            for coup in self.coup_possible_fantome(carte, k):
                distance = d[x] + 1
                (x3, y3) = coup
                voisin = [position[0] + x3, position[1] + y3]
                clef = tuple(voisin)
                if clef not in d or distance < d[clef]:
                    d[clef] = distance
                    nouv_dist = distance + self.heuristique(voisin, list(objectif))
                    atraiter[clef] = nouv_dist
                    parents[clef] = x

        trajet = self.chemin(parents, debut, objectif)
        if len(trajet) > 1:
            return trajet[1]
        else:
            return (a1 + x2, b1 + y2)

    @staticmethod
    def chemin(parents, debut, objectif):
        x = objectif
        path = [x]
        while x != debut:
            x = parents[x]
            path.append(x)
        path.reverse()
        return path

    def victoire(self, niveau):
        if self.score == niveau["maxscore"]:
            return True
        return False

    def joue(self, niveau: Niveau, coup_pac):
        (i, j) = coup_pac
        self.deplace_pacman(i, j)
        for ind in range(len(self.posfantomes)):
            print("astar")
            k, l = self.astar_for_ghost(ind, niveau["carte"])
            print((k, l))
            self.deplace_fantome(ind, k, l)
        self.mange_fruit()

    def mange_fruit(self):
        i, j = self.pospacman
        try:
            ind = self.fruits.index((i, j))
            self.score += 10
            del self.fruits[ind]
        except Exception:
            pass


if __name__ == "__main__":
    level = cartes.map5
    board = Board(level)
    fantomes_base = level["ghost"]
    u = 1
    while not board.fin_partie() and not board.victoire(level):
        board.affiche_board(level)
        time.sleep(1)
        while not board.vie_en_moins():
            (i, j) = random.choice(board.coup_possible(level["carte"]))
            print((i, j))
            print("test")
            board.joue(level, (i, j))
            print("test2")
            board.affiche_board(level)
            print()
            time.sleep(0.1)
        board.pospacman = level["pac"]
        board.posfantomes = fantomes_base.copy()
        print("test")
        board.reset_map(u)
        u += 1
        print()
