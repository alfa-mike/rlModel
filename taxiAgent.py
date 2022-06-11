import random
# import matplotlib.pyplot as plt
import math

GAMMA = 0.9
EPSILON = 0.00001
#####################################################

action = ['Up','Right','Down','Left','Drop','Pick']

# i,j = taxi position && k,l = passenger position
states = []
for i in range(5):
    for j in range(5):
        for k in range(5):
            for l in range(5):
                states.append((i,j,k,l,0))
                if i==k and j==l:
                    states.append((i,j,k,l,1))
                
utility = {}
for s in states:
    utility[s]=0
utilityU = utility.copy()
utility_policyiter = utility.copy()

policy = {}
for s in states: 
    policy[s]='Up'
policyP = policy.copy()

    

taxiPos = (4,0)                                     #random.choice([(x,y) for x in range(5) for y in range(5)])
possiblePos = [(0,0),(4,4)]                         #random.sample([(0,0) , (0,3) , (4,0) , (4,4)] , 2)
passPos , destPos = possiblePos[0],possiblePos[1] 
init = (taxiPos[0],taxiPos[1],passPos[0],passPos[1],0)
des = (destPos[0],destPos[1],destPos[0],destPos[1],0)
print(taxiPos,passPos,destPos)

####################################################

## Reward model
def reward (state, action):
    if action == 'Drop':
        if state[4] ==1:
            if destPos[0] == state[0] and destPos[1] == state[1]:
                return 20
        if state[0] !=state[2] or state[1] != state[3]:
            return -10
    if action == "Pick":
        if state[0] !=state[2] or state[1] != state[3]:
            return -10
    return -1


## Transition model
def transition(state, action,next_state):
    if action == "Drop":
        if state[0:4] == next_state[:4]:
            if state[0]!= state[2] or state[1]!= state[3]:
                if state == next_state:
                    return 1
            else:
                if state[4] ==1 and next_state[4] == 0:
                    return 1
                if state[4] == 0 and next_state[4] == 0:
                    return 1
        return 0
    
    elif action == "Pick":
        if state[:4] == next_state[:4]:
            if state[0]!=state[2] or state[1]!=state[3]:
                if state == next_state:
                    return 1
            else:
                if state[4] == 0:
                    if next_state[4] == 1:
                        return 1
                else:
                    if state[4] == 1 and next_state[4] == 1:
                        return 1   
        return 0

    else:
        if state[0] == 0 or state[0] == 1:
            if (state[1] == 0 and next_state[1] == 1) or (state[1] == 1 and next_state[1] == 0) or (state[1] == 2 and next_state[1] == 3) or (state[1] == 3 and next_state[1] == 2):
                return 0
        if state[0] == 3 or state[0] == 4:
            if (state[1] == 1 and next_state[1] == 2) or (state[1] ==2 and next_state[1] == 1):
                return 0
        if state[0] == 3 and state[1] == 3:
            if state == next_state:
                return 0
        if state[0] == 2:
            if state[1] == 1 or state[1] == 2 or state[1] == 3:
                if state == next_state:
                    return 0
        if action == "Up":
            if next_state[0] == state[0] +1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[0] == 4:
                    if state == next_state:
                        if state[1] == 3:
                            return 0.85
                        else:
                            return 0.9
                    else:
                        return 0.05 
                elif state[0] == 0:
                    if state[1] ==0:
                        if state == next_state:
                            return 0.15
                    else:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                elif state[0] == 1:
                    if state[1] == 0:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    else:
                        return 0.05
                elif state[0] == 2:
                    return 0.05
                elif state[0] == 3:
                    return 0.05
        if action == "Down":
            if next_state[0] == state[0] -1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[0] == 0:
                    if state[1] == 0:
                        if next_state == state:
                            return 0.95
                        else:
                            return 0.05
                    else:
                        if state ==next_state:
                            return 0.9
                        else:
                            return 0.05
                elif state[0] == 1:
                    if state[1] == 0:
                        if next_state == state:
                            return 0.1
                        else:
                            return 0.05
                    else:
                        return 0.05
                elif state[0] == 2:
                    return 0.05
                elif state[0] ==3:
                    return 0.05
                elif state[0] == 4:
                    if state[1] == 3:
                        return 0.05
                    else:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
        if action == "Left":
            if next_state[1] == state[1] -1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[1] == 0:
                    if state[0] == 0:
                        if next_state == state:
                            return 0.95
                        else:
                            return  0.05
                    elif state[0] == 1:
                        if next_state == state:
                            return 0.9
                        else:
                            return 0.05
                    elif state[0] == 2 or state[0] == 3:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
                    elif state[0] == 4:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                elif state[1] == 1:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                    if state[0] == 1:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
                    elif state[0] == 2 or state[0] == 3:
                        return 0.05
                    elif state[0] == 4:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                elif state[1] == 2:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    if state[0] == 1 or state[0] == 2:
                        return 0.05
                    elif state[0] == 3:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
                    elif state[0] == 4:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                elif state[1] == 3:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                    elif state[0] == 1:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
                    else:
                        return 0.05

            #change all 0.05 to 0.05 above
                elif state[1] == 4:
                    if state[0] == 0 or state[0] == 4:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    else:
                        return 0.05
        if action == "Right":
            if next_state[1] == state[1] +1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[1] == 0:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.95
                        else:
                            return 0.05
                    elif state[0] == 1:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                    elif state[0] == 4:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    else:
                        return 0.05
                if state[1] == 1:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    if state[0] == 1 or state[0] == 2:
                        return 0.05
                    if state[0] == 3:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
                    elif state[0] == 4:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                elif state[1] == 2:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.9
                    elif state[0] == 1:
                        if state == next_state:
                            return 0.85
                    elif state[0] == 4:
                        if state == next_state:
                            return 0.1

                    return 0.05
                elif state[1] == 3:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.1

                    return 0.05
                elif state[1] == 4:
                    if state == next_state:
                        if state[0] == 0 or state[0] == 4:
                            return 0.9
                        else:
                            return 0.85
                    else:
                        return 0.05


def transition2(state, action, next_state):
    if action == 'Drop':
        if state[0:4] == next_state[:4]:
            if state[0]!= state[2] or state[1]!= state[3]:
                if state == next_state:
                    return 1
            else:
                if state[4] ==1 and next_state[4] == 0:
                    return 1
                if state[4] == 0 and next_state[4] == 0:
                    return 1
                else:
                    return 0
        else:
            return 0
    elif action =='Pick':
        if state[:4] == next_state[:4]:
            if state[0]!=state[2] or state[1]!=state[3]:
                if state == next_state:
                    return 1
            else:
                if state[4] == 0:
                    if next_state[4] == 1:
                        return 1
                else:
                    if state[4] == 1 and next_state[4] == 1:
                        return 1
        return 0
    else:
        if state[0] == 0 or state[0] == 1 or state[0] == 2 or state[0] == 3:
            if (state[1] == 0 and next_state[1] == 1) or (state[1] == 1 and next_state[1] == 0) or (state[1] == 3 and next_state[1] == 4) or (state[1] == 4 and next_state[1] == 3) or (state[1] == 7 and next_state[1] == 8) or (state[1] == 8 and next_state[1] == 7) :
                return 0
        if state[0] == 4 or state[0] == 5 or state[0] == 6 or state[0] == 7:
            if (state[1] == 5 and next_state[1] == 6) or (state[1] == 6 and next_state[1] == 5):
                return 0
        if state[0] == 6 or state[0] == 7 or state[0] ==8 or state[0] == 9:
            if (state[1] == 2 and next_state[1] == 3) or (state[1] == 3 and next_state[1] == 2) or (state[1] == 7 and next_state[1] == 8) or (state[1] == 8 and next_state[1] == 7):
                return 0
        if action == 'Up':
            if next_state[0] == state[0] + 1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[0] == 0:
                    if state[1] == 0:
                        if state == next_state:
                            return 0.15
                    elif state[1] == 1 or state[1] == 3 or state[1] == 4 or state[1] == 7 or state[1] == 8 or state[1] == 9:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    else:
                        return 0.05
                elif state[0] in {1,2,3}:
                    if state[1] == 0:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    elif state[1] in {1,3,4,7,8,9}:
                        return 0.05
                    else:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                elif state[0] in {4,5}:
                    if state[1] in {0,5,6,9}:
                        return 0.05
                    else:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                elif state[0] in {6,7}:
                    if state[1] in {0,2,3,5,6,7,8,9}:
                        return 0.05
                    else:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                elif state[0] == 8:
                    if state[1] in {0,2,3,7,8,9}:
                        return 0.05
                    else:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                elif state[0] == 9:
                    if state[1] in {0,2,3,7,8,9}:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                    else:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
        
        if action == 'Down':
            if next_state[0] == state[0] -1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[0] == 0:
                    if state[1] == 0:
                        if state == next_state:
                            return 0.95
                        else:
                            return 0.05
                    elif state[1] in {1,3,4,7,8,9}:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                    elif state[1] in {2,5,6}:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
                elif state[0] in {1,2,3}:
                    if state[1] == 0:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    elif state[1] in {1,3,4,7,8,9}:
                        return 0.05
                    else:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                elif state[0] in {4,5}:
                    if state[1] in {0,5,6,9}:
                        return 0.05
                    else:
                        if state==next_state:
                            return 0
                        else:
                            return 0.05
                elif state[0] in {6,7}:
                    if state[1] in {1,4}:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                    else:
                        return 0.05
                elif state[0] == 8:
                    if state[1] in {0,2,3,7,8,9}:
                        return 0.05
                    else:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                elif state[0] == 9:
                    if state[1] in {0,2,3,7,8,9}:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    else:
                        return 0.05
        if action == 'Right':
            if next_state[1] == state[1] + 1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[1] == 0:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.95
                        else:
                            return 0.05
                    elif state[0] in {1,2,3}:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                    elif state[0] in {4,5,6,7,8}:
                        return 0.05
                    elif state[0] == 9:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                elif state[1] == 1:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.1
                        else:
                            return 0.05
                    elif state[0] in {1,2,3,9}:
                        return 0.05
                    elif state[0] in {4,5,6,7,8}:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                elif state[1] == 2:
                    if state[0] == 0:
                        return 0.05
                    elif state[0] in {1,2,3,4,5}:
                        if state == next_state:
                            return 0
                        else:
                            return 0.05
                    elif state[0] in {6,7,8}:
                        if state == next_state:
                            return 0.85
                        else:
                            return 0.05
                    else:
                        if state == next_state:
                            return 0.9
                        else:
                            return 0.05
                elif state[1] == 3:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.9
                    if state[0] in {1,2,3}:
                        if state == next_state:
                            return 0.85
                    if state[0] in {4,5}:
                        if state == next_state:
                            return 0
                    if state[0] == 9:
                        if state == next_state:
                            return 0.1
                    return 0.05
                elif state[1] ==4:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.1
                    if state[0] in {4,5,6,7,8}:
                        if state == next_state:
                            return 0
                    return 0.05
                elif state[1] == 5:
                    if state[0] in {1,2,3,8}:
                        if state == next_state:
                            return 0
                    if state[0] in {4,5,6,7}:
                        if state == next_state:
                            return 0.85
                    return 0.05
                elif state[1] == 6:
                    if state[0] in {1,2,3,8}:
                        if state == next_state:
                            return 0
                    
                    return 0.05
                elif state[1] == 7:
                    if state[0] in {0,9}:
                        if state == next_state:
                            return 0.9
                    if state[0] in {4,5}:
                        if state == next_state:
                            return 0
                    if state[0] in {1,2,3,6,7,8}:
                        if state == next_state:
                            return 0.85
                    return 0.05
                elif state[1] == 8:
                    if state[0] in {0,9}:
                        if state == next_state:
                            return 0.1
                    if state[0] in {4,5}:
                        if state == next_state:
                            return 0
                    return 0.05
                elif state[1] == 9:
                    if state[0] in {0,9}:
                        if state == next_state:
                            return 0.9
                    else:
                        if state == next_state:
                            return 0.85
                    return 0.05
        if action == 'Left':
            if next_state[1] == state[1] -1:
                return 0.85
            else:
                if state[0:4] == next_state[0:4] and state[4]!= next_state[4]:
                    return 0
                if state[1] == 0:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.95
                    elif state[0] in {1,2,3,9}:
                        if state == next_state:
                            return 0.9
                    else:
                        if state == next_state:
                            return 0.85
                    return 0.05   
                elif state[1] == 1:
                    if state[0] ==0:
                        if state == next_state:
                            return 0.9
                    if state[0] in {1,2,3}:
                        if state == next_state:
                            return 0.85
                    if state[0] in {4,5,6,7,8}:
                        if state == next_state:
                            return 0
                    return 0.05
                elif state[1] == 2:
                    if state[0] in {1,2,3,4,5}:
                        if state == next_state:
                            return 0
                    if state[0] == 9:
                        if state == next_state:
                            return 0.1
                    return 0.05
                elif state[1] == 3:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.1
                    elif state[0] in {4,5}:
                        if state == next_state:
                            return 0
                    elif state[0] in {6,7,8}:
                        if state == next_state:
                            return 0.85
                    elif state[0] == 9:
                        if state == next_state:
                            return 0.9
                    return 0.05
                elif state[1] == 4:
                    if state[0] == 0:
                        if state == next_state:
                            return 0.9
                    elif state[0] in {1,2,3}:
                        if state == next_state:
                            return 0.85
                    elif state[0] in {4,5,6,7,8}:
                        if state == next_state:
                            return 0
                    return 0.05
                elif state[1] == 5:
                    if state[0] in {1,2,3,8}:
                        if state == next_state:
                            return 0
                    return 0.05
                elif state[1] == 6:
                    if state[0] in {1,2,3,8}:
                        if state == next_state:
                            return 0
                    if state[0] in {4,5,6,7}:
                        if state == next_state:
                            return 0.85
                    return 0.05
                elif state[1] == 7:
                    if state[0] in {0,9}:
                        if state == next_state:
                            return 0.1
                    if state[0] in {4,5}:
                        if state == next_state:
                            return 0
                    return 0.05
                elif state[1] == 8:
                    if state[0] in {0,9}:
                        if state == next_state:
                            return 0.9
                    elif state[0] in {1,2,3,6,7,8}:
                        if state == next_state:
                            return 0.85
                    elif state[0] in {4,5} :
                        if state == next_state:
                            return 0
                    return 0.05
                elif state[1] == 9:
                    if state[0] in {0,9}:
                        if state == next_state:
                            return 0.1
                    return 0.05

####################################################

def calc_nxt(state):
    nxt = [state]
    a,b,c,d,e = state[0],state[1],state[2],state[3],state[4]
    if a==c and b==d:
        if e==1:
            nxt.append((a,b,c,d,e-1))
        if e==0:
            nxt.append((a,b,c,d,e+1))
    if e==0:
        if a==0:
            if b==0:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
            elif b==4:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
            else:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
                nxt.append((a,b+1,c,d,e))
        elif a==4:
            if b==0:
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
            elif b==4:
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
            else:
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
                nxt.append((a,b+1,c,d,e))
        else:
            if b==0:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
                nxt.append((a-1,b,c,d,e))
            elif b==4:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
                nxt.append((a-1,b,c,d,e))
            else:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
    else:
        if a==0:
            if b==0:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b+1,c,d+1,e))
            elif b==4:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b-1,c,d-1,e))
            else:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b-1,c,d-1,e))
                nxt.append((a,b+1,c,d+1,e))
        elif a==4:
            if b==0:
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b+1,c,d+1,e))
            elif b==4:
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b-1,c,d-1,e))
            else:
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b-1,c,d-1,e))
                nxt.append((a,b+1,c,d+1,e))
        else:
            if b==0:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b+1,c,d+1,e))
                nxt.append((a-1,b,c-1,d,e))
            elif b==4:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b-1,c,d-1,e))
                nxt.append((a-1,b,c-1,d,e))
            else:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b+1,c,d+1,e))
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b-1,c,d-1,e))

    return nxt

def calc_nxt2(state):
    nxt = [state]
    a,b,c,d,e = state[0],state[1],state[2],state[3],state[4]
    if a==c and b==d:
        if e==1:
            nxt.append((a,b,c,d,e-1))
        if e==0:
            nxt.append((a,b,c,d,e+1))
    if e==0:
        if a==0:
            if b==0:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
            elif b==9:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
            else:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
                nxt.append((a,b+1,c,d,e))
        elif a==9:
            if b==0:
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
            elif b==9:
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
            else:
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
                nxt.append((a,b+1,c,d,e))
        else:
            if b==0:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
                nxt.append((a-1,b,c,d,e))
            elif b==9:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
                nxt.append((a-1,b,c,d,e))
            else:
                nxt.append((a+1,b,c,d,e))
                nxt.append((a,b+1,c,d,e))
                nxt.append((a-1,b,c,d,e))
                nxt.append((a,b-1,c,d,e))
    else:
        if a==0:
            if b==0:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b+1,c,d+1,e))
            elif b==9:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b-1,c,d-1,e))
            else:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b-1,c,d-1,e))
                nxt.append((a,b+1,c,d+1,e))
        elif a==9:
            if b==0:
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b+1,c,d+1,e))
            elif b==9:
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b-1,c,d-1,e))
            else:
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b-1,c,d-1,e))
                nxt.append((a,b+1,c,d+1,e))
        else:
            if b==0:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b+1,c,d+1,e))
                nxt.append((a-1,b,c-1,d,e))
            elif b==9:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b-1,c,d-1,e))
                nxt.append((a-1,b,c-1,d,e))
            else:
                nxt.append((a+1,b,c+1,d,e))
                nxt.append((a,b+1,c,d+1,e))
                nxt.append((a-1,b,c-1,d,e))
                nxt.append((a,b-1,c,d-1,e))

    return nxt

def val_calc(s,action):
    sm = 0
    #print(calc_nxt(s))
    #print(action)
    for ele in calc_nxt(s): 
        #print(transition(s,action,ele))
        sm += (transition(s,action,ele)) * (reward(s,action) + (GAMMA * float(utility[ele])))
        
    return sm

def val_calc2(s,action):
    sm = 0
    for ele in calc_nxt(s):
        sm+= (transition(s,action,ele)) * (reward(s,action) + (GAMMA * float(utility_policyiter[ele])))
    return sm

def id(state):
    return ''.join(map(str,state))

def discounted_reward(policy,init_state, final_state, gamma):
    r = reward(init_state, policy[init_state])
    state = init_state
    for i in range(500):
        if state == final_state:
            break
        r += reward(state, policy[state])* (gamma**(i+1))
        next_states = calc_nxt(state)
        p = [transition(state, policy[state], next_state) for next_state in next_states]
        next_state = tuple(random.choices(next_states,p,k=1)[0])
        state = next_state
    return r


def policylosscnt(l):
    ploss = []
    fp = l[len(l)-1]
    for i in range(len(l)-1):
        s = 0
        for k,v in fp.items():
            s += (v-l[i][k])**2
        ploss.append(math.sqrt(s))            
    return ploss



def val_iteration(states):
    global utility
    no_iteration = 0
    max_normList = []
    while True:
        utilityperiter = utility.copy()
        delta = 0
        for s in states: 
            if s == (destPos[0],destPos[1],destPos[0],destPos[1],0):
                # no_iteration+=1
                continue
            
            max_val = float('-inf') 
            max_act = 'Up'
            for a in action:
                if max_val < val_calc(s,a):
                    max_val = val_calc(s,a)
                    max_act = a
            
            policy[s] = max_act
            utilityperiter[s] = max_val
            # print(utility[s], utilityperiter[s])

            if delta < abs(utilityperiter[s]-utility[s]):
                delta = abs(utilityperiter[s]-utility[s])

            # print(delta)

        utility = utilityperiter.copy()
        max_normList.append(delta)
        no_iteration+=1

        # print(delta)
        # print(((EPSILON * (1-GAMMA))/GAMMA))
        if delta < ((EPSILON * (1-GAMMA))/GAMMA):
            break

    return no_iteration , max_normList

def policy_iteration(states):
    global utility_policyiter
    global policyP
    list_utility = [utility_policyiter]
    no_iter = 0
    while True:
        while True:
            valueperiter = utility_policyiter.copy()
            delta = 0
            for s in states:
                if s[0] == (destPos[0],destPos[1],destPos[0],destPos[1],0):
                    continue
                #    break
                val = val_calc2(s,policyP[s])
                valueperiter[s] = val

                if delta < abs(valueperiter[s]-utility_policyiter[s]):
                    delta = abs(valueperiter[s]-utility_policyiter[s])

            
            utility_policyiter = valueperiter.copy()
            
            if delta < ((EPSILON * (1-GAMMA))/GAMMA):
                break
        
        next_policy = policyP.copy()
        for s in states:
            max_val = float('-inf')
            max_act = "Nil"
            for a in action:
                if max_val < val_calc2(s,a):
                    max_val = val_calc2(s,a)
                    max_act = a

            next_policy[s] = max_act

        list_utility.append(utility_policyiter)
        no_iter+=1  
        # print(no_iter)
        if next_policy!=policyP:
            policyP = next_policy.copy()
        else:
            break

    return no_iter,list_utility



Q = {}
for iii in states:
    for a in action:
        Q[(id(iii),a)] = 0

def q_learning(total_episodes, maxiter_episode, epsilon, alpha, gamma ):
    reward_list = list()
    global Q
    for episode in range(total_episodes):
        state = random.choice(states)
        # print(state)
        for iter in range(maxiter_episode):
            if random.uniform(0,1) < epsilon:
                act = random.choice(action)
            else:
                max_val = Q[(id(state),"Down")]
                max_act = "Down"
                for a in action:
                    val = Q[(id(state), a)]
                    if val>max_val:
                        max_val = val
                        max_act = a
                act = max_act
            
            #print(act,end="  ")
            tt = tt = calc_nxt(state)
            r = reward(state,act)
            p = [transition(state,act,nxt) for nxt in tt]
            
            
            #print(tt,end="   ")
            #print(p,end="   ")
            next_state = tuple(random.choices(tt,p,k=1)[0]) 

                
            #print(next_state)
            # print(Q[(id(state),act)])
            temp =  (1-alpha) * Q[(id(state), act)] 
            q_next = float("-inf")
            for a in action:
                # print(next_state)
                val = Q[(id(next_state), a)]
                if val>q_next:
                    q_next = val
            Q[(id(state), act)] = temp + alpha * (r + gamma * q_next)
            # print(Q[(id(state), act)])
            # print(Q[(id(state),act)])
            # print(" ")
            
            if next_state == (destPos[0],destPos[1],destPos[0],destPos[1],0):
                break
    
            state = next_state
        for k in states:
            op_a = "v"
            op_v = float('-inf')
            for a in action:
                if Q[(id(k),a)]>op_v:
                    op_a = a
                    op_v = Q[(id(k),a)]
            policy[k] = op_a
        if episode%50 == 49:
            lst1 = []
            for k in range(10):
                state1 = random.choice(states)
                a = discounted_reward(policy,state1, (destPos[0],destPos[1],destPos[0],destPos[1],0), gamma )
                lst1.append(a)
            reward_list.append(((episode+1), sum(lst1)/10))
    return reward_list

def q_learning2(total_episodes, maxiter_episode, epsilon, alpha, gamma ):
    reward_list = list()
    counter = 0
    global Q
    for episode in range(total_episodes):
        state = random.choice(states)
        for iter in range(maxiter_episode):
            if random.uniform(0,1) < epsilon/(1+counter):
                act = random.choice(action)
            else:
                max_val = Q[(id(state),"Down")]
                max_act = "Down"
                for a in action:
                    val = Q[(id(state), a)]
                    if val>max_val:
                        max_val = val
                        max_act = a
                act = max_act
            
            #print(act,end="  ")
            r = reward(state,act)
            tt = calc_nxt(state)
            p = [transition(state,act,nxt) for nxt in tt]
            
            #print(tt,end="   ")
            #print(p,end="   ")
            next_state = tuple(random.choices(tt,p,k=1)[0])    
            #print(next_state)
            # print(Q[(id(state),act)])
            temp =  (1-alpha) * Q[(id(state), act)] 
            q_next = float("-inf")
            for a in action:
                # print(next_state)
                val = Q[(id(next_state), a)]
                if val>q_next:
                    q_next = val
            Q[(id(state), act)] = temp + alpha * (r + gamma * q_next)
            # print(Q[(id(state), act)])
           
            # print(Q[(id(state),act)])
            # print(" ")
            counter += 1
            if next_state == [destPos[0],destPos[1],destPos[0],destPos[1],0]:
                break
    
            state = next_state    
        for k in states:
            op_a = "v"
            op_v = float('-inf')
            for a in action:
                if Q[(id(k),a)]>op_v:
                    op_a = a
                    op_v = Q[(id(k),a)]
            policy[k] = op_a
        if episode%50 == 49:
            lst1 = []
            for k in range(10):
                state1 = random.choice(states)
                a = discounted_reward(policy,state1, (destPos[0],destPos[1],destPos[0],destPos[1],0), gamma )
                lst1.append(a)
            reward_list.append(((episode+1), sum(lst1)/10))
    return reward_list

def sarsa(total_episodes, maxiter_episode, epsilon,alpha,gamma):
    reward_list = list()
    global Q
    for episode in range(total_episodes):
        state = random.choice(states)
        act = random.choice(action)
        for iter in range(maxiter_episode):
            if iter ==0:
                if random.uniform(0,1)<epsilon:
                    act = random.choice(action)
                else:
                    max_val = Q[(id(state),'Down')]
                    max_act = 'Down'
                    for a in action:
                        val = Q[(id(state), a)]
                        if val>max_val:
                            max_val = val
                            max_act = a
                    act = max_act
            # print(act, end=" ")
            r = reward(state,act)
            tt = calc_nxt(state)
            p = [transition(state,act,nxt) for nxt in tt]
            
            # print(tt,end="   ")
            # print(p)
            next_state = tuple(random.choices(tt,p,k=1)[0])
            temp = (1-alpha)*Q[(id(state), act)]

            if random.uniform(0,1) < epsilon:
                next_act = random.choice(action)
            else:
                max_val2 = Q[(id(next_state),'Down')]
                max_act2 = 'Down'
                for a in action:
                    val2 = Q[(id(next_state), a)] 
                    if val2>max_val2:
                        max_val2 = val2
                        max_act2 = a
                next_act = max_act2
            Q[(id(state), act)] = temp + alpha * (r + gamma *Q[(id(next_state), next_act)])
            if next_state == [destPos[0],destPos[1],destPos[0],destPos[1],0]:
                break
            state = next_state
            act = next_act

        for k in states:
            op_a = "v"
            op_v = float('-inf')
            for a in action:
                if Q[(id(k),a)]>op_v:
                    op_a = a
                    op_v = Q[(id(k),a)]
            policy[k] = op_a
        if episode%50 == 49:
            # print(episode)
            lst1 = []
            for k in range(100):
                state1 = random.choice(states)
                a = discounted_reward(policy,state1, (destPos[0],destPos[1],destPos[0],destPos[1],0), gamma )
                lst1.append(a)
            reward_list.append(((episode+1), sum(lst1)/100))
    return reward_list

def sarsa2(total_episodes, maxiter_episode, epsilon,alpha, gamma):
    global Q
    reward_list = list()
    counter = 0
    for episode in range(total_episodes):
        state = random.choice(states)
        act = random.choice(action)
        for iter in range(maxiter_episode):
            if iter ==0:
                if random.uniform(0,1)<epsilon/(1+counter):
                    act = random.choice(action)
                else:
                    max_val = Q[(id(state),'Down')]
                    max_act = 'Down'
                    for a in action:
                        val = Q[(id(state), a)]
                        if val>max_val:
                            max_val = val
                            max_act = a
                    act = max_act
            # print(act, end=" ")
            r = reward(state,act)
            tt = calc_nxt(state)
            p = [transition(state,act,nxt) for nxt in tt]
            
            # print(tt,end="   ")
            # print(p)
            next_state = tuple(random.choices(tt,p,k=1)[0])
            temp = (1-alpha)*Q[(id(state), act)]

            if random.uniform(0,1) < epsilon/(1+counter):
                next_act = random.choice(action)
            else:
                max_val2 = Q[(id(next_state),'Down')]
                max_act2 = 'Down'
                for a in action:
                    val2 = Q[(id(next_state), a)] 
                    if val2>max_val2:
                        max_val2 = val2
                        max_act2 = a
                next_act = max_act2
            counter+=1
            Q[(id(state), act)] = temp + alpha * (r + gamma *Q[(id(next_state), next_act)])
            if next_state == [destPos[0],destPos[1],destPos[0],destPos[1],0]:    
                break
            state = next_state
            act = next_act
        for k in states:
            op_a = "v"
            op_v = float('-inf')
            for a in action:
                if Q[(id(k),a)]>op_v:
                    op_a = a
                    op_v = Q[(id(k),a)]
            policy[k] = op_a
        if episode%50 == 49:
            lst1 = []
            for k in range(100):
                state1 = random.choice(states)
                a = discounted_reward(policy,state1, (destPos[0],destPos[1],destPos[0],destPos[1],0), gamma )
                lst1.append(a)
            reward_list.append(((episode+1), sum(lst1)/100))
    return reward_list


states_2 = []
for xx in range(10):
    for yy in range(10):
        for zz in range(10):
            for ww in range(10):
                states_2.append((xx,yy,zz,ww,0))
                if xx==yy and zz==ww:
                    states_2.append((xx,yy,zz,ww,1))

policy_2 = {}
for ii in states_2:
    policy_2[ii] = 'Up'

Q2 ={}
for kk in states_2:
    for ll in action:
        Q2[(id(kk), ll)] = 0

def newgrid(total_episodes, maxiter_episode, epsilon, alpha, gamma):
    reward_list = list()
    global Q2
    for episode in range(total_episodes):
        state = random.choice(states_2)
        for iter in range(maxiter_episode):
            if random.uniform(0,1) < epsilon:
                act = random.choice(action)
            else:
                max_val = Q2[(id(state),"Down")]
                max_act = "Down"
                for a in action:
                    val = Q2[(id(state), a)]
                    if val>max_val:
                        max_val = val
                        max_act = a
                act = max_act
            
            print(act,end="  ")
            tt = calc_nxt2(state)
            r = reward(state,act)
            p = [transition2(state,act,nxt) for nxt in tt]
            
            
            print(tt,end="   ")
            print(p,end="   ")
            next_state = tuple(random.choices(tt,p,k=1)[0])     
            print(next_state)
            # print(Q[(id(state),act)])
            temp =  (1-alpha) * Q2[(id(state), act)] 
            q_next = float("-inf")
            for a in action:
                # print(next_state)
                val = Q2[(id(next_state), a)]
                if val>q_next:
                    q_next = val
            Q2[(id(state), act)] = temp + alpha * (r + gamma * q_next)
            # print(Q[(id(state), act)])
            # print(Q[(id(state),act)])
            # print(" ")
            
            if next_state == (destPos[0],destPos[1],destPos[0],destPos[1],0):
                break
    
            state = next_state
        for k in states_2:
            op_a = "v"
            op_v = float('-inf')
            for a in action:
                if Q2[(id(k),a)]>op_v:
                    op_a = a
                    op_v = Q2[(id(k),a)]
            policy_2[k] = op_a
        if episode%100 == 99:
            lst1 = []
            for k in range(10):
                state1 = random.choice(states_2)
                a = discounted_reward(policy_2,state1, (destPos[0],destPos[1],destPos[0],destPos[1],0), gamma )
                lst1.append(a)
            reward_list.append(((episode+1), sum(lst1)/10))
    return reward_list


# def plt2a(m,l):
#     x = [i for i in range(m)]
#     plt.plot(x,l, color='blue', marker ='o', markersize = 4, label ='Discount factor = '+str(GAMMA))
#     plt.xlabel('Iteration index')
#     plt.ylabel('policy loss')  
#     plt.title('Relation between discount factor and rate of policy convergence')
#     plt.legend()
#     plt.show()

def give_action(cs,ns):
    if cs==ns:
        return "No Action"
    a,b,e = cs[0],cs[1],cs[4]
    v,w,z = ns[0],ns[1],ns[4]

    if cs[0:4]==ns[0:4]: 
        if e==0 and z==1:
            return "Pick"
        if e==1 and z==0:
            return "Drop" 

    elif v==a+1:
        return "Up"
    elif v==a-1:
        return "Down"
    elif w==b+1:
        return "Right"
    elif w==b-1:
        return "Left"


def simulation(init,dest,pol):
    nxt = init
    counter = 0
    while True:

        if nxt==dest or counter == 500:
            break
        a,b,c,d,e = nxt[0],nxt[1],nxt[2],nxt[3],nxt[4]
        act = pol[nxt]

    
        next_states = calc_nxt(nxt)
        p = [transition(nxt, act, st) for st in next_states]
        next = tuple(random.choices(next_states, p, k=1)[0])
        taken_action = give_action(nxt, next)
        print((a,b,c,d,e),act,taken_action)
        nxt = next
        counter+=1

# m,l = val_iteration(states)
# simulation(init,des,policy)
# print(m)
# plt2a(m,l)


# n,l = policy_iteration(states)
# simulation(init,des,policyP)
# print(n)
# pl = policylosscnt(l)
# plt2a(n,pl)


pp = sarsa(4000, 500, 0.1, 0.25, 0.99)
# for ele in pp:
#     print(ele)


# x = []
# y = []
# for i in p:
#     print(i)
#     x.append(i[0])
#     y.append(i[1])

# print(sum(y[len(y)-10:])/10)

# plt.plot(x, y)
# plt.xlabel('episode number')
# plt.ylabel('discounted rewards')
# plt.title('varying alpha, alpha = 0.5')
# plt.show()

simulation(init,des,policy)
    
    

