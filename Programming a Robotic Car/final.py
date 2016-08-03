#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maycon
#
# Created:     18/03/2012
# Copyright:   (c) Maycon 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

##
##road = [[80, 80, 80, 80, 80],
##         [60, 60, 60, 60, 60]]

road = [[50, 50, 50, 50, 50, 40,  0, 40, 50, 50,  0, 50, 50, 50, 50], # left lane: 50 km/h
        [40, 40, 40, 40,  0, 30, 20, 30,  0, 40, 40, 40, 40, 40, 40],
        [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]]

heuristic = [[0 for row in range(len(road[0]))] for col in range(len(road))]
cost = [[0 for row in range(len(road[0]))] for col in range(len(road))]

for i in range(len(cost)):
    for j in range(len(cost[0])):
        if road[i][j] == 0:
            cost[i][j]= 10000000.0
        else:
            cost[i][j]=1.0/road[i][j]

##for i in range(len(heuristic)):
##    for j in range(len(heuristic[0])):
##        if i>0:
##            heuristic[i][j]=heuristic[i-1][j]+1
##            heuristic[i][j]=heuristic[i][j]+1
##        if j>0:
##            heuristic[i][j]=heuristic[i][j-1]+1

axu=0
for i in range(len(heuristic)):
    for j in range(len(heuristic[0])):
        heuristic[i][j]=axu
        axu += 1



print heuristic


grid=[[0 for row in range(len(road[0]))] for col in range(len(road))]


for i in range(len(grid)):
    for j in range(len(grid[0])):
        if road[i][j] == 0:
            grid[i][j]= 1


##grid = [[0, 0, 0, 0, 0, 0],
##        [0, 1, 1, 1, 1, 0],
##        [0, 1, 0, 0, 0, 0],
##        [0, 1, 0, 0, 0, 0],
##        [0, 1, 0, 0, 1, 0]]
##
##heuristic = [[9, 8, 7, 6, 5, 4],
##            [8, 7, 6, 5, 4, 3],
##            [7, 6, 5, 4, 3, 2],
##            [6, 5, 4, 3, 2, 1],
##            [5, 4, 3, 2, 1, 0]]

init = [2, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # left shif
         [ 1, 0 ], # right shift
         [ 0, 1 ]] # go straight

delta_name = ['/', '\\', '->']



# ----------------------------------------
# modify code below
# ----------------------------------------

def search():
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1

    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    action = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]


    x = init[0]
    y = init[1]
    g = 0
    h=heuristic[x][y]
    f=g+h

    open = [[f, g, h, x, y]]

    found = False  # flag that is set when search is complet
    resign = False # flag set if we can't find expand
    count = 0

    while not found and not resign:
        if len(open) == 0:
            resign = True
        else:
            #remove node from list
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[3]
            y = next[4]
            g = next[1]
            expand[x][y] = count
            count += 1

            if x == goal[0] and y == goal[1]:
                found = True
            else:
                #expand winning element and add to new open list
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost[x2][y2]
                            h2=heuristic[x2][y2]
                            f2=g2+h2
                            open.append([f2, g2, h2, x2, y2])
                            closed[x2][y2] = 1
                            action[x2][y2]=i #used for printing the path (arrows)
    for i in range(len(expand)):
        print expand[i]
    policy=[['' for row in range(len(grid[0]))] for col in range(len(grid))]
    x=goal[0]
    y=goal[1]
    policy[x][y]='*'
    while x != init[0] or y != init[1]:
        x2= x - delta[action[x][y]][0]
        y2= y - delta[action[x][y]][1]
        #policy[x2][y2]=delta_name[action[x][y]]
        if (delta[action[x][y]][0] == -1) and (delta[action[x][y]][1] ==0):
              x=x2+1
              y=y2+1
              policy[x2][y2]='p'
        else:
            policy[x2][y2]='p'
            x=x2
            y=y2
    for i in range(len(policy)):
        print policy[i]

    return expand #Leave this line for grading purposes!


search()


delta = [[-1, 0 ], # left shif
         [ 1, 0 ], # right shift
         [ 0, 1 ]] # go straight