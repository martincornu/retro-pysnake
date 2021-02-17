"""
Creation: 15/01/21
Author: Martin Cornu

Scape-Game Saint-Etienne

Snake classic game modified. Toggle GPIO and display code on win.

"""

import time
from turtle import *
from random import randrange
from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
my_turtle = Turtle()
g_start = 0

def init():
    global g_start
    global food
    global aim
    global snake
    global my_turtle
    
    g_start = 0
    food = vector(0, 0)
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    head = snake[-1].copy()
    head.move(aim)
    my_turtle.color('black')
    my_turtle.write("Press space to start", font=("Arial", 16, "bold"), align="center")
    move()

def start():
    global g_start
    if g_start == 0:
        g_start = 1
        my_turtle.undo()

def change(x, y):
    "Change snake direction."
    aim.x = x
    aim.y = y

def inside(head):
    "Return True if head inside boundaries."
    return -200 < head.x < 190 and -200 < head.y < 190

def move():
    global g_start
    global my_turtle
    
    if g_start == 1:
        "Move snake forward one segment."
        head = snake[-1].copy()
        head.move(aim)

        if not inside(head) or head in snake:
            clear()
            my_turtle.color('red')
            my_turtle.write("GAMEOVER", font=("Arial", 25, "bold"), align="center")
            time.sleep(1)
            my_turtle.clear()
            init()
            return

        snake.append(head)

        if head == food:
            print('Snake:', len(snake))
            food.x = randrange(-15, 15) * 10
            food.y = randrange(-15, 15) * 10
        else:
            snake.pop(0)
            # display code and set an output to high if len > ...
            if len(snake) > 1:
                clear()
                my_turtle.color('green')
                my_turtle.write("WIN! CODE : 43120", font=("Arial", 25, "bold"), align="center")
                return

        clear()

        for body in snake:
            square(body.x, body.y, 9, 'black')

        square(food.x, food.y, 9, 'green')
        update()

    ontimer(move, 100)
    

setup(420, 420, 370, 0)
hideturtle()
my_turtle.hideturtle()
tracer(False)
listen()
onkey(lambda: start(), 'space')
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
init()
done()
