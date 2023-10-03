import jeu as jeu
import numpy as np
from random import choice
import copy
import random


class Node:


    def __init__(self,m,p):
        self.move=m
        self.parent=p
        self.win=0
        self.visits=0
        self.children = []


    def est_feuille(self):
        if len(self.children)==0:
            return True
        return False
    
    def selection(self):
        enfants=self.children
        ind=0
        max=Node(enfants[0],self).uct()
        for i in range(len(enfants)):
            if Node(enfants[i],self).uct()>max:
                ind=i
                max=Node(enfants[i],self).uct
        if Node(enfants[ind],self).est_feuille():
            return enfants[ind]
        return Node(enfants[ind],self).selection()

    def expansion(self,etat):
        position=etat["pacman"]
        if not jeu.vie_en_moins(etat):
            for enfant in jeu.coup_possible(etat,position):
                nc=Node(enfant,self)
                self.children.append(nc)

    def backprogation(self,resultat):
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
        return (wi/ni + np.sqrt(2)*np.sqrt(np.log(Ni)/ni))



def rollout(etat):
    state=copy.deepcopy(etat)
    compteur=0
    while not jeu.vie_en_moins(state) or jeu.victoire(state):
        position=state["pacman"]
        coups=jeu.coup_possible(state,position)
        (i,j)=random.choice(coups)
        k,l=jeu.astar_for_ghost(state)
        jeu.deplace(state,"pacman",i,j)
        state["f"]=[k,l]
        jeu.deplace(state,"f",k,l)
        jeu.mange_fruit(state)
        compteur+=1
    if jeu.victoire(state) or compteur>=6:
        return 1
    else:
        return 0
        
        
        

def MCTS1(etat):
    root_node=Node(None,None)
    while not jeu.vie_en_moins(etat):
        n,s=root_node, copy.deepcopy(etat)
        while not n.est_feuille():
            n = n.selection()
            #jouer le coup
            (i,j)=n
            k,l=jeu.astar_for_ghost(s)
            jeu.deplace(s,"pacman",i,j)
            s["f"]=[k,l]
            jeu.deplace(s,"f",k,l)
            jeu.mange_fruit(s)
            #jouer le coup
            n.expansion(s)
        n = n.selection()
        while not jeu.vie_en_moins(s):
            s = rollout(s)
        resultat= rollout(s)
        while n.a_parent():
            n.updtate(resultat)
            n = n.parent
    return n.parent
        






















class PacManBoard(Node):
    def find_children(etat):
        position=etat["pacman"]
        if jeu.coup_possible(etat,position)==[]:   
            return set()
        return jeu.coup_possible(etat,position)


    def find_random_child(etat):
        if jeu.coup_possible(etat,position)==[]:   
            return None
        position=etat["pacman"]
        i,j=choice(jeu.coup_possible(etat,position))
        return jeu.deplace(etat,"pacman",i,j)


    def reward(etat):
        if jeu.vie_en_moins(etat):
            return 0
        if jeu.victoire(etat):
            return 1
        else:
            return 0
    
    





    

def enfants1(node):
    childs=node.children
    for child in childs:
        child.parent=node
        child.depth=node.depth+1
    if node.est_feuille():
        return node
    return node.best_child()

def uct1(node):
    wi=node.win
    ni=node.depth
    t=len(node.children)
    return (wi/ni + np.sqrt(t/ni))


def selection1(node):
    enfants=node.children
    ind=0
    max=uct(enfants[0])
    for i in range(len(enfants)):
        if uct(enfants[i])>max:
            ind=i
            max=uct(enfants[i])
    if est_feuille(enfants[ind]):
        return enfants[ind]
    return selection(enfants[ind])
    

    
    
    
    
    
    
    
    
    



