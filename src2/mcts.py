import jeu as jeu

class Node:
    def __init__(self,etat):
        self.etat=etat
        self.win=0
        self.lose=0
        self.played=0
        self.children=jeu.coup_possible(etat,etat["pacman"])
        self.parent=None
    
    
    def est_feuille(self):
        if len(self.children)==0:
            return True
        return False
    

def selection(node):
    childs=node.children
    for child in childs:
        child.parent=node
    if node.est_feuille():
        return Node
    return node.best_child()





def rollout(node):
    state=node.etat
    while not jeu.vie_en_moins(state) and not jeu.victoire(state):
        i,j=jeu.get_score(state)
        k,l=jeu.astar_for_ghost(state)
        jeu.deplace(state,"pacman",i,j)
        state["f"]=[k,l]
        jeu.mange_fruit(state)
    node.played+=1
    if jeu.vie_en_moins(state):
        node.lose+=1
        return "lose"
    else:
        node.win+=1
        return "win"
    

def backpropagation(self,result):
    

    
    
    
    
    
    
    
    
    



