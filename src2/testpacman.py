import copy
import time
import numpy as np
import heapdict as hd
import cartes_pac as cartes
import random


class Node:
    def __init__(self, move, etat):
        self.move = move
        self.win = 0
        self.visits = 0
        self.children = {}
        # clef=coup, valeur=node
        self.est_terminal = False
        self.etat = etat

    def est_feuille(self):
        etat = self.etat
        if victoire(etat) or vie_en_moins(etat):
            return True
        return False

    def selection(self, etat):
        if self.est_feuille():
            return self
        if len(self.children) == 0:
            return self
        enfants = self.children
        ind = 0
        maxi = enfants[0].uct()
        for i in range(len(enfants)):
            if enfants[i].uct() > maxi:
                ind = i
                maxi = enfants[i].uct
        if enfants[ind].est_feuille(etat):
            return enfants[ind]
        return enfants[ind].selection(etat)

    def expansion(self):
        if self.est_feuille():
            return 0
        etat = self.etat
        coups = coup_possible(etat, etat["pacman"])
        if len(self.children) != len(coups):
            for coup in coups:
                if coup not in self.children:
                    state = copy.deepcopy(etat)

                    noeud = Node(coup)
                    resultat = rollout(noeud)
                    noeud.update(resultat)
                    self.children[coup] = noeud

    def update(self, resultat):
        self.visits += 1
        self.win += resultat

    def a_parent(self):
        if self.parent == None:
            return False
        return True

    def uct(self):
        wi = self.win
        ni = self.visits
        Ni = self.parent.visits
        if Ni == 0:
            return 0
        else:
            return wi / ni + np.sqrt(2) * np.sqrt(np.log(Ni) / ni)


def rollout(etat):
    state = copy.deepcopy(etat)
    compteur = 0
    while not vie_en_moins(state) or victoire(state):
        position = state["pacman"]
        coups = coup_possible(state, position)
        (i, j) = random.choice(coups)
        (k, l) = astar_for_ghost(state)
        deplace(state, "pacman", i, j)
        state["f"] = [k, l]
        deplace(state, "f", k, l)
        mange_fruit(state)
        compteur += 1
    if victoire(state) or compteur >= 6:
        return 1
    else:
        return 0


def MCTS1(etat):
    pass


"""    
    root_node=Node(None,None)
    compteur=0
    while not vie_en_moins(etat) and compteur <5:
        n,s=root_node, copy.deepcopy(etat)
        n.expansion(state)
        compteur2=0
        while not n.est_feuille(state) and compteur2<5:
            n = n.selection(state)
            #jouer le coup
            mouv=n.move
            i,j=mouv
            k,l=astar_for_ghost(s)
            deplace(s,"pacman",i,j)
            s["f"]=[k,l]
            deplace(s,"f",k,l)
            mange_fruit(s)
            #jouer le coup
            n.expansion(s)
            compteur2+=1
        n = n.selection(state)
        print(1)
        resultat= rollout(s)
        while n.a_parent():
            n.updtate(resultat)
            n = n.parent
            print(2)
        compteur+=1
    return n.parent

"""


def init_board():
    board_s = carte["carte"]
    res = []
    for line in board_s:
        res_ligne = []
        for x in line:
            res_ligne.append(x)
        res.append(res_ligne)
    return res


class Board:
    def __init__(self, depart_pacman, depart_fantomes, carte):
        self.fruits = carte["fruits"]
        self.pospacman = depart_pacman
        self.posfantomes = [depart_fantomes[0], depart_fantomes[1], depart_fantomes[2]]
        self.nombre_vies = 3
        self.score = 0

    def affiche_board(self, carte):
        board = self.board_avec_persos(carte["carte"])
        for line in board:
            for x in line:
                print(x, end="")
            print()

    def board_avec_persos(self, carte):
        board = copy.deepcopy(carte)
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
        self.pospcman = [position[0] + i, position[1] + j]

    def deplace_fantome(self, k, i, j):
        self.posfantomes[k] = [i, j]

    def vie_en_moins(self):
        for k in range(3):
            if self.pospacman == self.posfantomes[k]:
                return True
        return False

    def reset_map(self, i):
        print("Une vie en moins")
        self.nombre = 3 - i
        print("nombre de vies =", self.nombre_vies)
        time.sleep(1)

    def fin_partie(self):
        if self.nombre_vies == 0:
            return True
        return False

    def coup_possible(self, carte):
        position = self.pospacman
        board = carte
        mouvement = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        # haut,droite,bas,gauche
        res = []
        for mouv in mouvement:
            newpos = [position[0] + mouv[0], position[1] + mouv[1]]
            if (
                0 <= newpos[0] < len(board)
                and 0 <= newpos[1] < len(board[0])
                and board[newpos[0]][newpos[1]] != "■"
            ):
                res.append(tuple(mouv))
        return res

    def coup_possible_fantome(self, carte, k):
        position = self.posfantomes[k]
        board = carte
        mouvement = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        # haut,droite,bas,gauche
        res = []
        for mouv in mouvement:
            newpos = [position[0] + mouv[0], position[1] + mouv[1]]
            if (
                0 <= newpos[0] < len(board)
                and 0 <= newpos[1] < len(board[0])
                and board[newpos[0]][newpos[1]] != "■"
            ):
                res.append(tuple(mouv))
        return res

    @staticmethod
    def heuristique(posfantome, pospacman):
        x1, y1 = posfantome
        x2, y2 = pospacman
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def astar_for_ghost(self, k, carte):
        debut = tuple(self.posfantomes[k])
        objectif = tuple(self.pospacman)
        atraiter = hd.heapdict()
        atraiter[debut] = 0
        parents = {}
        d = {}
        parents[debut] = None
        d[debut] = 0
        while len(atraiter) > 0:
            x, _ = atraiter.popitem()
            position = list(x)
            if x == objectif:
                break
            for coup in self.coup_possible_fantome(carte, k):
                distance = d[x] + 1
                voisin = [position[0] + coup[0], position[1] + coup[1]]
                clef = tuple(voisin)
                if clef not in d or distance < d[clef]:
                    d[clef] = distance
                    nouv_dist = distance + self.heuristique(voisin, list(objectif))
                    atraiter[clef] = nouv_dist
                    parents[clef] = x
        if objectif not in parents:
            return (0, 0)
        trajet = self.chemin(parents, debut, objectif)
        if len(trajet) > 1:
            return trajet[1]
        else:
            return (0, 0)

    @staticmethod
    def chemin(parents, debut, objectif):
        x = objectif
        path = [x]
        while x != debut:
            x = parents[x]
            path.append(x)
        path.reverse()
        return path

    def victoire(self, carte):
        if self.score == carte["maxscore"]:
            return True
        return False

    def joue(self, carte, coup_pac):
        (i, j) = coup_pac
        self.deplace_pacman(i, j)
        for ind in range(len(self.posfantomes)):
            print("astar")
            k, l = self.astar_for_ghost(ind, carte["carte"])
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
    carte = cartes.map5
    board = Board(carte["pac"], carte["ghost"], carte)
    u = 1
    while not board.fin_partie() and not board.victoire(carte):
        board.affiche_board(carte)
        time.sleep(1)
        while not board.vie_en_moins():
            (i, j) = random.choice(board.coup_possible(carte["carte"]))
            print("test")
            board.joue(carte, (i, j))
            print("test2")
            board.affiche_board(carte)
            print()
            time.sleep(0.1)
        u += 1
        print()
