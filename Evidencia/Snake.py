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

def randcolor():
    return random.choice(["green", "blue", "yellow", "purple", "black"])

def add_block():
    tries = 0
    while True:
        tries += 1
        new_block = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)
        conflict = False
        for b in snake + obstacles + [food]:
            if new_block.x == b.x and new_block.y == b.y:
                conflict = True
                break
        if not conflict:
            obstacles.append(new_block)
            break
        if tries > 200:
            break

def _sync_colors():
    if len(snake_colors) < len(snake):
        for _ in range(len(snake) - len(snake_colors)):
            snake_colors.append(randcolor())
    elif len(snake_colors) > len(snake):
        extra = len(snake_colors) - len(snake)
        del snake_colors[0:extra]

timeDelay = 250
timeDecrement = 15
minTimeDelay = 50

def move():
    global timeDelay, special_food
    head = snake[-1].copy()
    head.move(aim)

    if not inside(head) or head in snake or head in obstacles:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        tries = 0
        while True:
            tries += 1
            new_fx = randrange(-15, 15) * 10
            new_fy = randrange(-15, 15) * 10
            conflict = False
            for b in snake + obstacles:
                if new_fx == b.x and new_fy == b.y:
                    conflict = True
                    break
            if not conflict:
                food.x = new_fx
                food.y = new_fy
                break
            if tries > 500:
                break

        # --- COMIDA ESPECIAL ---
        if random.random() < 0.2:
            special_food = True
        else:
            special_food = False

        if special_food:
            for _ in range(3):
                snake_colors.append(randcolor())
            special_food = False
        else:
            snake_colors.append(randcolor())
        # ---------------------

        add_block()

        if timeDelay > minTimeDelay:
            timeDelay = max(minTimeDelay, timeDelay - timeDecrement)
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
    for body, color_seg in zip(snake, snake_colors):
        square(body.x, body.y, 9, color_seg)

    # --- Dibujar comida ---
    if special_food:
        square(food.x, food.y, 9, randcolor())
    else:
        square(food.x, food.y, 9, 'green')

    for block in obstacles:
        square(block.x, block.y, 9, 'red')

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
