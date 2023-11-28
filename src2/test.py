import numpy as np

print(2 * [1, 2])

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


random.choice(board.coup_possible(carte))


