import random
from random import randrange, choice
from turtle import *
from freegames import square, vector

# --- Estado del juego ---
food = vector(0, 0)
special_food = False  # NUEVO
snake = [vector(10, 0)]
snake_colors = ["green"]  # lista paralela: color de cada segmento (misma longitud que `snake`)
aim = vector(0, -10)
fooddir = vector(10, 0)
foodspeed = 400
obstacles = []

def change(x, y):
    aim.x = x
    aim.y = y

def inside(head):
    return -200 < head.x < 190 and -200 < head.y < 190


def move():
    global timeDelay, special_food
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake or head in obstacles:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)
"""Aquí esta la funcionalidad de cada comida, si aumenta 1 o si reduce 1 o 3, también verifica que no se encuentren en la misma posición"""
"""Angel Enirque Montes Pacheco"""
    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        if len(snake) > 1:
            snake.pop(0)
        if len(snake_colors) > 1:
            snake_colors.pop(0)

    if len(snake_colors) != len(snake):
        if len(snake_colors) < len(snake):
            for _ in range(len(snake) - len(snake_colors)):
                snake_colors.append(randcolor())
        else:
            extra = len(snake_colors) - len(snake)
            del snake_colors[0:extra]

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, timeDelay)

def foodmove():
    global fooddir
    if random.random() < 0.2:
        fooddir = choice([vector(10, 0), vector(-10, 0), vector(0, 10), vector(0, -10)])
    next_food = food + fooddir
    if inside(next_food):
        food.move(fooddir)
    else:
        fooddir = choice([vector(10, 0), vector(-10, 0), vector(0, 10), vector(0, -10)])
    ontimer(foodmove, foodspeed)

# --- Main ---
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

# decidir comida inicial especial
if random.random() < 0.2:
    special_food = True

move()
foodmove()
done()
