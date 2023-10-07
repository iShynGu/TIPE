import copy
import time
import numpy as np
import heapdict as hd
import cartes_pac as map
import random

class Node:


    def __init__(self,move,etat):
        self.move=move
        self.win=0
        self.visits=0
        self.children = {}
        #clef=coup, valeur=node
        self.est_terminal=False
        self.etat=etat

    def est_feuille(self):
        etat=self.etat
        if victoire(etat) or vie_en_moins(etat):
            return True
        return False
    
    def selection(self,etat):
        if self.est_feuille():
            return self
        if len(self.children)==0:
            return self
        enfants=self.children
        ind=0
        maxi=enfants[0].uct()
        for i in range(len(enfants)):
            if enfants[i].uct()>maxi:
                ind=i
                maxi=enfants[i].uct
        if enfants[ind].est_feuille(etat):
            return enfants[ind]
        return enfants[ind].selection(etat)

    def expansion(self):
        if self.est_feuille():
            return 0
        etat=self.etat
        coups=coup_possible(etat,etat["pacman"])
        if len(self.children)!=len(coups):
            for coup in coups:
                if coup not in self.children:
                    state=copy.deepcopy(etat)
                    
                    noeud=Node(coup)
                    resultat=rollout(noeud)
                    noeud.update(resultat)
                    self.children[coup]=noeud

                    

    
    
    
    def update(self,resultat):
        self.visits+=1
        self.win+=resultat

    def a_parent(self):
        if self.parent == None:
            return False
        return True
    
    def uct(self):
        wi=self.win
        ni=self.visits
        Ni=self.parent.visits
        if Ni==0:
            return 0
        else:
            return (wi/ni + np.sqrt(2)*np.sqrt(np.log(Ni)/ni))



def rollout(etat):
    state=copy.deepcopy(etat)
    compteur=0
    while not vie_en_moins(state) or victoire(state):
        position=state["pacman"]
        coups=coup_possible(state,position)
        (i,j)=random.choice(coups)
        (k,l)=astar_for_ghost(state)
        deplace(state,"pacman",i,j)
        state["f"]=[k,l]
        deplace(state,"f",k,l)
        mange_fruit(state)
        compteur+=1
    if victoire(state) or compteur>=6:
        return 1
    else:
        return 0
        
        
        

def MCTS1(etat):
    pass
'''    
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

'''


carte=map.map5


depart_pacman=carte["pac"]
depart_fantomes=carte["ghost"]

def init_board():
    board_s=carte["carte"]
    res=[]
    for line in board_s:
        res_ligne=[]
        for x in line:
            res_ligne.append(x)
        res.append(res_ligne)
    return res
    
def init_game():
    res={}
    res["board"]=init_board()
    res["pacman"]=depart_pacman
    res["f0"]=depart_fantomes[0]
    res["f1"]=depart_fantomes[1]
    res["f2"]=depart_fantomes[2]
    res["nbr_vies"]=3
    res["score"]=0
    return res
    
def affiche(etat):
    board=board_avec_persos(etat,[["pacman","ᗧ"],["f0","ᗣ"],["f1","ᗣ"],["f2","ᗣ"]])
    for line in board:
        for x in line:
            print(x, end='')
        print()

def board_avec_persos(etat,persos):
    board = copy.deepcopy(etat["board"])
    for perso in persos:
        i,j=etat[perso[0]]
        board[i][j]=perso[1]
    return board
    

def deplace(etat,perso,i,j):
    PosP=etat[perso]
    etat[perso]=[PosP[0]+i,PosP[1]+j]
    
def vie_en_moins(etat):
    if etat["pacman"]==etat["f"]:
        return True
    return False

def reset_map(i,etat):
    print("Une vie en moins")
    etat["nbr_vies"]=3-i
    print("nombre de vies =", etat["nbr_vies"])
    time.sleep(1)


def fin_partie(etat):
    if etat["nbr_vies"]==0:
        return True
    return False
    
def coup_possible(etat,position):
    PosP=position
    board=etat["board"]
    mouvement=[[-1,0],[0,1],[1,0],[0,-1]]
    #haut,droite,bas,gauche
    res=[]
    for mouv in mouvement:
        newpos=[PosP[0]+mouv[0],PosP[1]+mouv[1]]
        if 0 <= newpos[0] < len(board) and 0 <= newpos[1] < len(board[0]) and board[newpos[0]][newpos[1]] != '■':
            res.append(tuple(mouv))
    return res

def meilleur_coup_pac(etat):
    PosP=etat["pacman"]
    possible_moves=coup_possible(etat,PosP)
    PosF=etat["f"]
    move_distances=[]
    for move in possible_moves:
        newpos=[PosP[0]+move[0],PosP[1]+move[1]]
        move_distances.append([newpos[0]-PosF[0],newpos[1]-PosF[1]])
    max_ind=0
    max_dist=np.sqrt(move_distances[0][0]**2+move_distances[0][1]**2)
    for o in range(len(possible_moves)):
        dist=np.sqrt(move_distances[o][0]**2+move_distances[o][1]**2)
        if dist > max_dist:
            max_ind=o
            max_dist=dist
    return possible_moves[max_ind]


def cherche_les_points(etat):
    PosP=etat["pacman"]
    possible_moves=coup_possible(etat,PosP)
    board=etat["board"]
    res=[]
    for move in possible_moves:
        newpos=[PosP[0]+move[0],PosP[1]+move[1]]
        if board[newpos[0]][newpos[1]]=="•":
            res.append(move)
    return res
#faire dijkstra pour le cherche_les_points



def heuristique(etat):
    x1, y1 = etat["f"]
    x2, y2 = etat["pacman"]
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def astar_for_ghost(etat):
    debut = tuple(etat["f"])
    objectif = tuple(etat["pacman"])
    atraiter = hd.heapdict()
    atraiter[debut] = 0
    parents = {}
    d = {}
    parents[debut] = None
    d[debut] = 0
    while len(atraiter)>0:
        x,fx = atraiter.popitem()
        position=list(x)
        if x == objectif:
            break
        for coup in coup_possible(etat, position):
            distance = d[x] + 1
            voisin=[position[0]+coup[0],position[1]+coup[1]]
            clef=tuple(voisin)
            if clef not in d or distance < d[clef]:
                d[clef] = distance
                nouv_dist = distance + heuristique({"f": voisin, "pacman": list(objectif)})
                atraiter[clef] = nouv_dist
                parents[clef] = x
    if objectif not in parents:
        return (0, 0)
    trajet = chemin(parents, debut, objectif)
    if len(trajet) > 1:
        return trajet[1]
    else:
        return (0,0)

def chemin(parents, debut, objectif):
    x = objectif
    path = [x]
    while x != debut:
        x = parents[x]
        path.append(x)
    path.reverse()
    return path


def victoire(etat):
    board=etat["board"]
    for i in range(len(board)):
        for j in board[i]:
            if j=="•":
                return False
    return True


def joue(state,coup_pac):
        (i,j)=coup_pac
        k,l=astar_for_ghost(state)
        deplace(state,"pacman",i,j)
        state["f"]=[k,l]
        mange_fruit(state)



def mange_fruit(etat):
    board=etat["board"]
    i,j=etat["pacman"]
    if board[i][j]=="•":
        etat["score"]+=10
        board[i][j]=" "

state=copy.deepcopy(init_game())
u=1
while not fin_partie(state) and not victoire(state):
    affiche(state)
    time.sleep(1)
    while not vie_en_moins(state):
        (i,j)=MCTS1(state)
        #k,l=coup_possible(state,state["f"])[0]
        k,l=astar_for_ghost(state)
        deplace(state,"pacman",i,j)
        state["f"]=[k,l]
        #deplace(state,"f",k,l)
        mange_fruit(state)
        affiche(state)
        print()
        time.sleep(0.1)
    state["pacman"]=depart_pacman
    state["f"]=depart_fantome
    reset_map(u,state)
    u+=1
    print()

print("score =",state["score"])
if fin_partie(state):
    print("vous avez perdu")
elif victoire(state):
    print("vous avez gagné")