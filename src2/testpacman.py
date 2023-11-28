import copy
import time
import numpy as np
import heapdict as hd
import cartes_pac as cartes
import random
import json

Niveau = dict


with open("astar_pregen.txt", "r") as r:
    coups_a_faire_fantome = json.loads(r.read())


class Node:
    def __init__(self, move: tuple, plateau, parent):
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

    # détermine si un noeud est une feuille
    def est_feuille(self, scoremax: int):
        if self.plateau.victoire(scoremax) or self.plateau.vie_en_moins():
            return True
        return False

    def a_parent(self):
        if self.parent is None:
            return False
        return True

    def selection(self, scoremax: int, carte1: list[str]):
        if self.est_feuille(scoremax):
            return

        coups_possibles = self.plateau.coup_possible(carte1)
        if len(coups_possibles) == 0:
            return
        if len(self.children) < len(coups_possibles):
            for coup in coups_possibles:
                if coup not in self.children:
                    self.expansion(
                        coup, carte1, scoremax
                    )  # crée un noeud pour un coup possible non exploré
        else:
            meilleur_enfant = (
                self.uct()
            )  # si tous les noeuds fils sont créés alors choisis le meilleur selon la fonction uct
            meilleur_enfant.selection(scoremax, carte1)

    def expansion(self, coup: tuple, carte1: list[str], scoremax: int):
        plateau1 = copy.deepcopy(self.plateau)
        plateau1.joue(coup)
        parent = self
        new_node = Node(coup, plateau1, parent)
        resultat = rollout(
            new_node.plateau, carte1, scoremax
        )  # fait une simulation pour donner une valeur au noeud
        new_node.update(resultat)
        n = self
        while n.a_parent():
            n.update(resultat)
            n = n.parent
        n.update(resultat)
        self.children[coup] = new_node

    def update(self, resultat: int):
        self.visits += 1
        self.win += resultat

    @staticmethod
    def aux_uct(wi: int, ni: int, Ni: int):
        if Ni == 0:
            return 0
        else:
            return wi / ni + np.sqrt(2) * np.sqrt(np.log(Ni) / ni)

    def uct(self):  # renvoie le meilleur noeud
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


def rollout(
    plateau, carte: list[str], scoremax: int
):  # effectue une simulation en jouant aléatoirement
    plateau1 = copy.deepcopy(plateau)
    compteur = 0
    points_debuts = plateau.score
    while (
        not (plateau1.vie_en_moins() or plateau1.victoire(scoremax)) and compteur < 100
    ):
        coups = plateau1.coup_possible(carte)
        (i, j) = random.choice(coups)
        plateau1.joue((i, j))
        compteur += 1
    if plateau1.victoire(scoremax):
        return 100000000  # maximise le choix du noeud si il est gagnant
    else:
        return (
            compteur + (plateau1.score - points_debuts) / 10
        )  # donne autant de score pour un déplacement que pour un point


def MCTS1(root_node, nb_simulations: int):
    niveau = cartes.map5
    carte = niveau["carte"]
    scoremax = niveau["maxscore"]
    for _ in range(nb_simulations):
        root_node.selection(scoremax, carte)
    return root_node.uct()


class Board:
    def __init__(self, niveau: dict):
        self.fruits = niveau["fruits"].copy()
        self.pospacman = niveau["pac"].copy()
        self.posfantomes = niveau["ghost"].copy()
        self.nombre_vies = 3
        self.score = 0

    def affiche_board(self, niveau: dict):
        board = self.board_avec_persos(niveau["carte"])
        for line in board:
            for x in line:
                print(x, end="")
            print()

    def board_avec_persos(self, niveau: dict):
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

    def sur_un_fantome(
        self, newpos: list[int]
    ):  # vérifie si pacman est sur un fantome dans une position possible
        for k in range(len(self.posfantomes)):
            if self.posfantomes[k] == newpos:
                return True
        return False

    def coup_possible(
        self, carte: list[str]
    ):  # renvoie la liste des coups possibles pour pacman
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

    def coup_possible_fantome(
        self, carte: list[str], k: int
    ):  # renvoie la liste des coups possibles pour le fantome k
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
    def heuristique(posfantome: list[int], pospacman: list[int]):
        x1, y1 = posfantome
        x2, y2 = pospacman
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def astar_for_ghost(self, k: int, carte: list[str]):
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
    def chemin(parents: dict, debut: tuple, objectif: tuple):
        x = objectif
        path = [x]
        while x != debut:
            if x not in parents:
                return []
            x = parents[x]
            path.append(x)
        path.reverse()
        return path

    def victoire(self, scoremax: int):
        if self.score == scoremax:
            return True
        return False

    def meilleur_coup_fantome(self, posfantome: list[int], pospac: list[int]):
        return coups_a_faire_fantome[
            f"{posfantome[0]},{posfantome[1]},{pospac[0]},{pospac[1]}"
        ]

    def joue(self, coup_pac: tuple):
        (i, j) = coup_pac
        self.deplace_pacman(i, j)
        if not self.sur_un_fantome(self.pospacman):
            for ind in range(len(self.posfantomes)):
                [k, l] = self.meilleur_coup_fantome(
                    self.posfantomes[ind], self.pospacman
                )
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
            noeud = MCTS1(noeud, 50)
            (i, j) = noeud.move
            print(board.coup_possible(carte))
            # print(start_node)
            board.joue((i, j))
            board.affiche_board(level)
            print()
            # time.sleep(0.1)
        board.pospacman = level["pac"]
        board.posfantomes = fantomes_base.copy()
        board.reset_map(u)
        u += 1
        print()
    print("c'est fini")
