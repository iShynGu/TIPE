import jeu as jeu
import numpy as np

class Node:
    def __init__(self,etat):
        self.etat=etat
        self.win=0
        self.lose=0
        self.played=0
        self.children=jeu.coup_possible(etat,etat["pacman"])
        self.parent=None
        self.depth=0
    
    def enfant(self,parent1):
        self.etat=parent1.etat
        self.win=0
        self.lose=0
        self.played=0
        self.children=[]
        self.parent=parent1
        self.depth=parent1.depth + 1
    
    def create_child(self):
        parent=self
        child=self.enfant(self,parent)
        self.children.append(child)

    
def est_feuille(node):
    if len(node.children)==0:
        return True
    return False
    

def enfants(node):
    childs=node.children
    for child in childs:
        child.parent=node
        child.depth=node.depth+1
    if node.est_feuille():
        return node
    return node.best_child()

def uct(node):
    wi=node.win
    ni=node.depth
    t=len(node.children)
    return (wi/ni + np.sqrt(t/ni))


def selection(node):
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

def expansion (node):
    
    


def rollout(node):
    
    

def backpropagation(self,result):
    

    
    
    
    
    
    
    
    
    



