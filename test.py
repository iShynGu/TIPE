def victoire(state):
    board=state["board"]
    for i in range(len(board)):
        for j in board[i]:
            if j=="•":
                return False
    return True

def init_board():
    board_s=[
"■■■■■■■■■■■■",
"■••••••••••■",
"■•■•■■••■••■",
"■•■•■•••■■•■",
"■••••••••••■",
"■■■■■■■■■■■■"
]
    res=[]
    for line in board_s:
        res_ligne=[]
        for x in line:
            res_ligne.append(x)
        res.append(res_ligne)
    return res

board=init_board()

print(True == victoire({"board" : board}))