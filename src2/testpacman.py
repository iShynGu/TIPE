import copy
import time
import numpy as np
import heapdict as hd
import cartes_pac as cartes
import random

Niveau = dict


class Node:
    def __init__(self, move, plateau, parent):
        self.move = move
        self.win = 0
        self.visits = 0
        self.children = {}
        # clef=coup, valeur=node
        self.est_terminal = False
        self.plateau = plateau
        self.parent = parent

    def __repr__(self):
        return f"{self.parent} {self.children}"

    def est_feuille(self, scoremax):
        if self.plateau.victoire(scoremax) or self.plateau.vie_en_moins():
            return True
        return False

    def a_parent(self):
        if self.parent is None:
            return False
        return True

    def selection(self, scoremax, carte1):
        if self.est_feuille(scoremax):
            # print("test")
            return

        coups_possibles = self.plateau.coup_possible(carte1)
        if len(coups_possibles) == 0:
            # print("test1")
            return
        if len(self.children) < len(coups_possibles):
            for coup in coups_possibles:
                if coup not in self.children:
                    self.expansion(coup, carte1, scoremax)
        else:
            meilleur_enfant = self.uct()
            meilleur_enfant.selection(scoremax, carte1)

    def expansion(self, coup, carte1, scoremax):
        plateau1 = copy.deepcopy(self.plateau)
        plateau1.joue(carte1, coup)
        parent = self
        new_node = Node(coup, plateau1, parent)
        resultat = rollout(new_node.plateau, carte1, scoremax)

        new_node.update(resultat)
        n = self
        while n.a_parent():
            n.update(resultat)
            n = n.parent
        n.update(resultat)
        self.children[coup] = new_node

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
        return self.children[res]


def rollout(plateau, carte, scoremax):
    plateau1 = copy.deepcopy(plateau)
    compteur = 0
    points_debuts = plateau.score
    while not plateau1.vie_en_moins() or plateau1.victoire(scoremax) and compteur < 100:
        coups = plateau1.coup_possible(carte)
        (i, j) = random.choice(coups)
        plateau1.joue(carte, (i, j))
        compteur += 1
    if plateau1.victoire(scoremax):
        return 100000000
    else:
        return compteur + (plateau1.score - points_debuts) / 10


def MCTS1(plateau, root_node, nb_simulations):
    niveau = cartes.map5
    carte = niveau["carte"]
    scoremax = niveau["maxscore"]
    for _ in range(nb_simulations):
        root_node.selection(scoremax, carte)
    return root_node.uct()


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
            ligne[j] = "ᗣ"
            board[i] = "".join(ligne)

        return board

    def deplace_pacman(self, i, j):
        position = self.pospacman
        self.pospacman = [position[0] + i, position[1] + j]

    def deplace_fantome(self, k, i, j):
        self.posfantomes[k] = [i, j]

    def vie_en_moins(self):
        for k in range(len(self.posfantomes)):
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

    def sur_un_fantome(self, newpos):
        for k in range(len(self.posfantomes)):
            if self.posfantomes[k] == newpos:
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
            if x not in parents:
                return []
            x = parents[x]
            path.append(x)
        path.reverse()
        return path

    def victoire(self, scoremax):
        if self.score == scoremax:
            return True
        return False

    def joue(self, carte, coup_pac):
        (i, j) = coup_pac
        self.deplace_pacman(i, j)
        if not self.sur_un_fantome(self.pospacman):
            for ind in range(len(self.posfantomes)):
                k, l = self.astar_for_ghost(ind, carte)
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
    carte = level["carte"]
    board = Board(level)
    fantomes_base = level["ghost"]
    score_max = level["maxscore"]
    u = 1
    start_node = Node(None, board, None)
    while not board.fin_partie() and not board.victoire(score_max):
        board.affiche_board(level)
        time.sleep(1)
        noeud = start_node
        while not board.vie_en_moins():
            noeud = MCTS1(board, noeud, 500)
            (i, j) = noeud.move
            print(board.coup_possible(carte))
            # print(start_node)
            board.joue(carte, (i, j))
            board.affiche_board(level)
            print()
            time.sleep(0.1)
        board.pospacman = level["pac"]
        board.posfantomes = fantomes_base.copy()
        board.reset_map(u)
        u += 1
        print()
