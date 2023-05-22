with open("prout","r") as file:
    lines=file.readlines()
    l=[]
    calories=0
    for i in lines:
        i=i.strip()
        if i=="":
            l.append(calories)
            calories=0
        else:
            calories+=int(i)
    print(sum(sorted(l)[-3:]))
            
