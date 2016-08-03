#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maycon
#
# Created:     27/02/2012
# Copyright:   (c) Maycon 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()
#Modify the previous code so that the robot senses red twice.

p=[0.2, 0.2, 0.2, 0.2, 0.2]
world=['green', 'red', 'red', 'green', 'green']
measurements = ['red', 'red']
motions = [1,1]
pHit = 0.6
pMiss = 0.2
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1


##
##def move(p, U):
##    q = []
##    for i in range(len(p)):
##        s = pExact * p[(i-U) % len(p)]
##        s = s + pOvershoot * p[(i-U-1) % len(p)]
##        s = s + pUndershoot * p[(i-U+1) % len(p)]
##        q.append(s)
##    return q
##
##for k in range(len(measurements)):
##    p = sense(p, measurements[k])
##    p = move(p, motions[k])
##
##print p
##



colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

p = []

##[0,0] - no move
##[0,1] - right
##[0,-1] - left
##[1,0]- down
##[-1,0]- up


def initial_state(p,world):
    a=[]
    for i in range(len(world)+1):
        a.append(1./(len(world)*len(world[0])))
    for i in range(len(world)):
        p.append(a)
    return p

p=initial_state(p,colors)



##def checagem(p,Z,world,a):
##    b=0
##    while b < len(world)+1:
##        if Z==(world[a][b]):
##            p[a][b]=(p[a][b])*sensor_right
##        else:
##            p[a][b]=(p[a][b])*(1-sensor_right)
##        b=b+1
##    return p
##
##def sense(p, Z, world):
##    a=0
##    while a < len(world):
##        p=checagem(p,Z,world,a)
##        a=a+1
##    return p



def sense(p, Z, world):
    a=0
    while a < len(world):
        b=0
        while b < len(world)+1:
            if Z==(world[a][b]):
               p[a][b]=(p[a][b])*sensor_right
            else:
                (p[a][b])=(p[a][b])*(1-sensor_right)
            b=b+1
        a=a+1
    return p

p=sense (p,'red',colors)




#Your probability array must be printed
#with the following code.

def find_last(data,target):
    a=data.find(target)
    if a==-1:
        return a
    else:
        while a!=-1:
            b=data.find(target,a+1)
            if b==-1:
                return a
            a=data.find(target, b+1)
        return b

p=['H','e','l','l','o']
q=p
print p
q[0]='Y'
print p
