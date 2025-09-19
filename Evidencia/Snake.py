"""Snake, classic arcade game.

Exercises

1. How do you make the snake faster or slower?
2. How can you make the snake go around the edges?
3. How would you move the food?
4. Change the snake to respond to mouse clicks.
"""

from random import randrange
from turtle import *

from freegames import square, vector

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)


def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y


def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

"""Función que determina un color aleatorio para la serpiente, de entre ciertos colores, predeterminados"""
"""Angel Enirque Montes Pacheco"""
def snakeColor():
    color = ["purple","blue","yellow"]
    color_random = random.choice(color)
    return color_random

"""Función que verifica que las posiciones entre las "comidas" sea distinta"""
"""Angel Enirque Montes Pacheco"""
def verifyRandom(a,b,f,g,x,y):
    if a == f and b == g:
        while a == f and b == g:
            a = randrange(15,-15) * 10
        return a
    elif a == x and b == y:
        while a == x and b == y:
            b = randrange(15,-15) * 10
        return b
    elif f == x and g == y:
        while f == x and g == y:
            g = randrange(15,-15) * 10
        return g
    else:
        return a

"""Variable que contiene un color aleatorio"""
"""Angel Enirque Montes Pacheco"""
snakeColor_random = snakeColor()

def move():
    """Move snake forward one segment."""
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)
"""Aquí esta la funcionalidad de cada comida, si aumenta 1 o si reduce 1 o 3, también verifica que no se encuentren en la misma posición"""
"""Angel Enirque Montes Pacheco"""
    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-15, 15) * 10      
        food.x = verifyRandom(food.x,food.y,boomFood.x,boomFood.y,trashFood.x,trashFood.y)
        food.y = randrange(-15, 15) * 10
    elif head == boomFood:
        if len(snake) > 3:
            del snake[-4:]
            print('Snake:', len(snake))
            boomFood.x = randrange(-15, 15) * 10
            boomFood.y = randrange(-15, 15) * 10
            boomFood.y = verifyRandom(food.x,food.y,boomFood.x,boomFood.y,trashFood.x,trashFood.y)
        else:
            square(head.x, head.y,9,"red")
            update()
            return
    elif head == trashFood:
        if len(snake) > 2:
            del snake[-2:]
            print('Snake:', len(snake))
            trashFood.x = randrange(-15, 15) * 10
            trashFood.y = randrange(-15, 15) * 10
            trashFood.y = verifyRandom(food.x,food.y,boomFood.x,boomFood.y,trashFood.x,trashFood.y)
        else:
            square(head.x, head.y,9,"red")
            update()
            return
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, snakeColor_random)

    square(food.x, food.y, 9, 'green')
    """Angel Enirque Montes Pacheco"""
    square(boomFood.x, boomFood.y, 9, 'black')
    square(trashFood.x, trashFood.y, 9, 'red')
    update()
    ontimer(move, 100)


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')
move()
done()