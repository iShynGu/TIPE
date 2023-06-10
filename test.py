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


board=init_board()
print(board[4][6])