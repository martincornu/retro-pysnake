"""
Creation: 15/01/21
Author: Martin Cornu

Scape-Game Saint-Etienne

Snake classic game modified. Toggle GPIO and display code on win.

"""
DESKTOP_PC = 0  # set to 1 to run script on pc and not use GPIO

import time

if DESKTOP_PC == 0:
    import RPi.GPIO as GPIO

import turtle
from turtle import *
from random import randrange
from freegames import square, vector

COLOR_THEME = 0     # set to 0 for black/white color theme
                    # set to 1 for white/green/red color theme
OUTPUT_PIN = 21
CODE = "43120"
LED_PIN = 20
SNAKE_LEN = 10
SNAKE_SIZE = 15
SNAKE_SPEED = 100
CHANGE_DIR_TIME_MIN = 150  # minimum time (ms) between change direction

RECTANGLE_H = 480   # 384, 480, 600 , 800
RECTANGLE_W = 600   # 480, 600, 750, 1000
INSIDE_PADDING = SNAKE_SIZE  # apply inside padding to make sure snake does not go out limits.

if DESKTOP_PC == 0:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
my_turtle = Turtle()
g_start = 0
g_direction = "down"      # current snake direction
g_change_dir_last_ts = 0  # last change direction timestamp in ms
wn=turtle.Screen()

if COLOR_THEME == 0:
    wn.bgcolor("black")

# draw rectangle to delimit the game (borders)
t = turtle.Turtle()
t.width(4)
if COLOR_THEME == 1:
    t.color("white")
elif COLOR_THEME == 0:
    t.color("black")
t.setpos(-(RECTANGLE_W/2), -(RECTANGLE_H/2))
if COLOR_THEME == 0:
    t.color("white")
elif COLOR_THEME == 1:
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

    if DESKTOP_PC == 0:
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
    if COLOR_THEME == 1:
        my_turtle.color('black')
    elif COLOR_THEME == 0:
        my_turtle.color('white')
    
    my_turtle.write("Press button to start", font=("Arial", 35, "bold"), align="center")
    
    move()

def start():
    global g_start
    if g_start == 0:
        g_start = 1
        my_turtle.undo()

def change(x, y):
    global g_direction
    global g_change_dir_last_ts
    
    # get current time in ms
    end = time.time_ns() / 1000000
    # change direction only if last change was older than CHANGE_DIR_TIME_MIN.
    # this is to avoid unwanted changes which leads to gameovers.
    if (end - g_change_dir_last_ts) > CHANGE_DIR_TIME_MIN:
        print("change")
        g_change_dir_last_ts = end
        
        # first find aim direction
        if x == 10 and y == 0:
            l_aimDirection = "right"
        elif x == -10 and y == 0:
            l_aimDirection = "left"
        elif x == 0 and y == 10:
            l_aimDirection = "up"
        elif x == 0 and y == -10:
            l_aimDirection = "down"
            
        # check if aim direction is the opposite way to avoid
        # miswanted game over.
        if ((g_direction == "right" and l_aimDirection != "left")
             or (g_direction == "left" and l_aimDirection != "right")
             or (g_direction == "up" and l_aimDirection != "down")
             or (g_direction == "down" and l_aimDirection != "up")):
            
            # if not opposite, then change snake direction
            aim.x = x
            aim.y = y
            g_direction = l_aimDirection
    else:
        print("change too fast")


def inside(head):
    "Return True if head inside boundaries."
    return -((RECTANGLE_W/2)-INSIDE_PADDING) < head.x < ((RECTANGLE_W/2)-INSIDE_PADDING) and -((RECTANGLE_H/2)-INSIDE_PADDING) < head.y < ((RECTANGLE_H/2)-INSIDE_PADDING)

def move():
    global g_start
    global my_turtle
    
    if g_start == 1:
        "Move snake forward one segment."
        head = snake[-1].copy()
        
        head.move(aim)

        if not inside(head) or head in snake:
            keys_deactivate()
            clear()
            if COLOR_THEME == 1:
                my_turtle.color('red')
            elif COLOR_THEME == 0:
                my_turtle.color('white')
            my_turtle.write("GAMEOVER", font=("Arial", 35, "bold"), align="center")
            time.sleep(1)
            my_turtle.clear()
            init()
            keys_activate()
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
                keys_deactivate()
                clear()
                if COLOR_THEME == 1:
                    my_turtle.color('green')
                elif COLOR_THEME == 0:
                    my_turtle.color('white')
                my_turtle.write("LASER ACTIF\n\n CODE " + CODE, font=("Arial", 35, "bold"), align="center")
                if DESKTOP_PC == 0:
                    GPIO.output(LED_PIN, 1)
                    GPIO.output(OUTPUT_PIN, 1)
                keys_activate()
                return

        clear()

        for body in snake:
            if COLOR_THEME == 1:
                square(body.x, body.y, SNAKE_SIZE, 'black')
            elif COLOR_THEME == 0:
                square(body.x, body.y, SNAKE_SIZE, 'white')
 
        if COLOR_THEME == 1:
            square(food.x, food.y, SNAKE_SIZE, 'green')
        elif COLOR_THEME == 0:
            square(food.x, food.y, SNAKE_SIZE, 'white')
        update()

    ontimer(move, SNAKE_SPEED)
    
def keys_activate():
    onkey(lambda: start(), 'space')
    onkey(lambda: change(10, 0), 'Right')
    onkey(lambda: change(-10, 0), 'Left')
    onkey(lambda: change(0, 10), 'Up')
    onkey(lambda: change(0, -10), 'Down')
    listen()
    
def keys_deactivate():
    onkey(None, 'space')
    onkey(None, 'Right')
    onkey(None, 'Left')
    onkey(None, 'Up')
    onkey(None, 'Down')
    
window = Screen()
window.setup(width=1.0, height=1.0, startx=None, starty=None)
hideturtle()
my_turtle.hideturtle()
tracer(False)
keys_activate()
init()
done()
