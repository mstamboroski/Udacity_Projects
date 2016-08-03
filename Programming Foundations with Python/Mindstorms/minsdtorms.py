__author__ = 'Maycon'

import turtle

def draw_square():
    window = turtle.Screen()
    window.bgcolor("red")

    brad = turtle.Turtle()
    brad.shape("turtle")
    brad.speed(1)

    for i in range(4):
        brad.right(90)
        brad.forward(100)

    window.exitonclick()

draw_square()
