"""
Creation: 15/01/21
Author: Martin Cornu

Scape-Game Saint-Etienne

Snake classic game modified. Toggle GPIO and display code on win.

"""

import time
import RPi.GPIO as GPIO
import turtle
from turtle import *
from random import randrange
from freegames import square, vector

OUTPUT_PIN = 21
CODE = "43120"
LED_PIN = 20
SNAKE_LEN = 30

RECTANGLE_H = 800
RECTANGLE_W = 1000

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(OUTPUT_PIN, GPIO.OUT)

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
my_turtle = Turtle()
g_start = 0

# draw rectangle to delimit the game (borders)
t = turtle.Turtle()
t.width(4)
t.color("white")
t.setpos(-(RECTANGLE_W/2), -(RECTANGLE_H/2))
t.color("black")
t.forward(RECTANGLE_W)
t.left(90)
t.forward(RECTANGLE_H)
t.left(90)
t.forward(RECTANGLE_W)
t.left(90)
t.forward(RECTANGLE_H)
t.left(90)
t.hideturtle()

def init():
    global g_start
    global food
    global aim
    global snake
    global my_turtle

    # clear gpios
    GPIO.output(LED_PIN, 0)
    GPIO.output(OUTPUT_PIN, 0)
    # init snake
    g_start = 0
    food = vector(0, 0)
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    head = snake[-1].copy()
    head.move(aim)
    # init screen
    my_turtle.color('black')
    my_turtle.write("Press button to start", font=("Arial", 35, "bold"), align="center")
    
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
    return -(RECTANGLE_W/2) < head.x < (RECTANGLE_W/2) and -(RECTANGLE_H/2) < head.y < (RECTANGLE_H/2)

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
            my_turtle.write("GAMEOVER", font=("Arial", 35, "bold"), align="center")
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
            if len(snake) > SNAKE_LEN:
                clear()
                my_turtle.color('green')
                my_turtle.write("WIN! CODE : " + CODE, font=("Arial", 35, "bold"), align="center")
                GPIO.output(LED_PIN, 1)
                GPIO.output(OUTPUT_PIN, 1)
                return

        clear()

        for body in snake:
            square(body.x, body.y, 9, 'black')

        square(food.x, food.y, 9, 'green')
        update()

    ontimer(move, 50)

    
window = Screen()
window.setup(width=1.0, height=1.0, startx=None, starty=None)
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
