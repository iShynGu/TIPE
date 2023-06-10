import copy
import time


def init_board():
    board_s=[
"************",
"*..........*",
"*.*.**..*..*",
"*.*.*...**.*",
"*..........*",
"************"
]
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
    res["pacman"]=[4,6]
    res["f"]=[1,1]
    res["nbr_vies"]=3
    res["score"]=0
    return res
    
def affiche(etat):
    board=board_avec_persos(etat,[["pacman","ᗧ"],["f","ᗣ"]])
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
    
def coup_possible(etat,perso):
    PosP=etat[perso]
    board=etat["board"]
    mouvement=[[-1,0],[0,1],[1,0],[0,-1]]
    #haut,droite,bas,gauche
    res=[]
    for mouv in mouvement:
        newpos=[PosP[0]+mouv[0],PosP[1]+mouv[1]]
        if 0 <= newpos[0] < len(board) and 0 <= newpos[1] < len(board[0]) and board[newpos[0]][newpos[1]] != '*':
            res.append(mouv)
    return res

def mange_fruit(etat):
    board=etat["board"]
    i,j=etat["pacman"]
    if board[i][j]==".":
        etat["score"]+=10
        board[i][j]=" "

state=copy.deepcopy(init_game())
u=1
while not fin_partie(state):
    while not vie_en_moins(state):
        i,j=coup_possible(state,"pacman")[0]
        k,l=coup_possible(state,"f")[0]
        deplace(state,"pacman",i,j)
        deplace(state,"f",k,l)
        mange_fruit(state)
        affiche(state)
        print()
        time.sleep(0.5)
    state["pacman"]=[4,6]
    state["f"]=[1,1]
    reset_map(u,state)
    u+=1
    print()
print("score =",state["score"])
print("vous avez perdu")