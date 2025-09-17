"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to mouse clicks.
"""


import random
from random import randrange, choice
from turtle import *

from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
fooddir = vector(10,0)
foodspeed = 400
obstacles = []

def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y


def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

"""Angel Enrique Montes Pacheco"""
def randcolor():
    """Select a random color"""
    color = ["green","blue","yellow","purple","black"]
    random_color = random.choice(color)
    return random_color

skinSneak = randcolor()
skinFood = randcolor()

def skinSnakecolor(s,f):
    if s != f:
        return s
    else:
        s = randcolor()
        skinSnakecolor(s,f)
        return s
    
def skinFoodcolor(s,f):
    if s != f:
        return f
    else:
        f = randcolor()
        skinFoodcolor(s,f)
        return f


"""David Rangel Monsiváis"""
def add_block():
    """Add a block (obstacle) at a random free position."""
    while True:
        new_block = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)
        # Compara coordenadas
        conflict = False
        for b in snake + obstacles + [food]:
            if new_block.x == b.x and new_block.y == b.y:
                conflict = True
                break
        if not conflict:
            obstacles.append(new_block)
            break


"""Modificado para add_block"""
def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake or head in obstacles:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
        global timeDelay

        add_block()

        if timeDelay > minTimeDelay: #Carlos Arias Capetillo 
            timeDelay -= timeDecrement

    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, skinSnakecolor(skinSneak,skinFood))

    square(food.x, food.y, 9, skinFoodcolor(skinFood,skinSneak))

    for block in obstacles:
        square(block.x, block.y, 9, 'red')

    update()
    ontimer(move, timeDelay)

timeDelay = 100
timeDecrement = 5
minTimeDelay = 50

"""Carlos Almaraz Arrambide"""
def snakemove():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        snake.pop(0)
    draw()
    ontimer(snakemove, 100)  

def foodmove():
    global fooddir

    if random.random() < 0.2:
        fooddir = choice([vector(10,0), vector(-10,0), vector(0,10), vector(0,-10)])

    next_food = food + fooddir
    if inside(next_food):
        food.move(fooddir)
    else:
        fooddir = choice([vector(10,5), vector(-10,5), vector(5,10), vector(5,-10)])
    draw()
    ontimer(foodmove,foodspeed)


def draw():
    clear()
    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    update()

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
snakemove()
foodmove()
move()
done()
