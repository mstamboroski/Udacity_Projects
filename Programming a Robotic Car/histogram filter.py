#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Maycon
#
# Created:     06/04/2012
# Copyright:   (c) Maycon 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

def main():
    pass

if __name__ == '__main__':
    main()

colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']


motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]


def show(p):
    for i in range(len(p)):
        print p[i]


##[0,0] - no move
##[0,1] - right
##[0,-1] - left
##[1,0]- down
##[-1,0]- up


sensor_right = 0.7  # Probabilidade da leitura do sensor estar correta

sensor_wrong = 1.0 - sensor_right # Probabilidade complementar do erro do sensor

p_move = 0.8 # Probabilidade da acao motion ser executada corretamente, se motion falhar, neste caso, o robo nao se move

p_stay = 1.0 - p_move # Probabilidade de falha no movimento



def sense(p, colors, measurements):
    aux=[[0.0 for row in range(len(p[0]))]for col in range(len(p))] # inicia a probabilidade posterior como sendo 0.0 em tudo
    s=0.0
    for i in range(len(p)):
        for j in range(len(p[i])):
            hit = (measurements == colors[i][j]) # Se a leitura for correta, ele retorna 1.0, senao, 0.0
            aux[i][j] = p[i][j] * (hit*sensor_right + (1-hit)*sensor_wrong) # Faz essa soma usando a variavel booleana hit, se hit==1 entao usa-se a probabilidade de leitura correta, se hit==0 usa-se a probabilidade da leitura errada do sensor. Isso eh multiplicado pela probabilidade da celula[i][j] que eu estou
            s += aux[i][j] # somo todos os valores de aux
    for i in range(len(aux)):
        for j in range(len(p[i])):
            aux[i][j] /= s #Normalizo aux para ter uma probabilidade total de 1.0
    return aux



def move(p, motion):
    aux=[[0.0 for row in range(len(p[0]))]for col in range(len(p))] # inicia a probabilidade posterior como sendo 0.0 em tudo

    for i in range(len(p)):
        for j in range(len(p[i])):
            #Calculo as celulas de onde o robo pode ter vindo
            aux[i][j]=(p_move * p[(i - motion[0]) % len(p)][(j - motion[1]) % len(p[i])]) + (p_stay * p[i][j])
            #(p_move * p[(i - motion [0]) indica que o movimento deu certo, o % eh devido ao fato do mundo ser ciclico
            # Caso nao haja movimento, usa-se a probabilidade p_stay vezes e probabilidade inicial da celula em questao
    return aux





# Main routine

# Checagem de erros
if len(measurements) != len(motions):
    raise ValueError, "error in size of measurements/motions vector"

# Distribuicao uniforme da probabilidade inicial:
pinit=1.0 / float(len(colors)) / float(len(colors[0]))
p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]


for k in range (len(measurements)):
    p=move(p,motions[k])  # Calculo uma nova distribuicao de probabilidades devido ao movimento
    p=sense(p, colors, measurements[k]) #Com a probabilidade calculada anterior, eu atualizo ela com uma leitura do sensor

#Your probability array must be printed
#with the following code.
show(p)

