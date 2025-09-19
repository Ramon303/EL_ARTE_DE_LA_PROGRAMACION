import random
from random import randrange, choice
from turtle import *
from freegames import square, vector

# --- Estado del juego ---
food = vector(0, 0)
special_food = False  # NUEVO: comida especial que hace crecer 3 bloques
snake = [vector(10, 0)]
snake_colors = ["green"]  # lista paralela: color de cada segmento (misma longitud que snake)
aim = vector(0, -10)
fooddir = vector(10, 0)
foodspeed = 400
obstacles = []
cpu_snake = []            #NUEVO: variables del cpu
cpu_aim = vector(10, 0)   
cpu_active = False        
spawn_score = 5

# NUEVO: variables para comidas bomba
boomFood = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)
trashFood = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)

def change(x, y):
    """Change snake direction."""
    aim.x = x
    aim.y = y

def inside(head):
    """Return True if head inside boundaries."""
    return -200 < head.x < 190 and -200 < head.y < 190

"""Carlos Guillermo Almaraz Arrambide"""
def move_cpu():
    """Movimiento de la serpiente CPU"""
    global cpu_aim

    if not cpu_snake:
        return

    head = cpu_snake[-1].copy()

    # Estrategia simple: moverse hacia la comida
    if abs(food.x - head.x) > abs(food.y - head.y):
        cpu_aim.x = 10 if food.x > head.x else -10
        cpu_aim.y = 0
    else:
        cpu_aim.y = 10 if food.y > head.y else -10
        cpu_aim.x = 0

    head.move(cpu_aim)

    if not inside(head) or head in cpu_snake:
        return  # CPU muere si choca contra sí mismo o bordes

    cpu_snake.append(head)

    if head == food:
        food.x = randrange(-15, 15) * 10
        food.y = randrange(-15, 15) * 10
    else:
        cpu_snake.pop(0)

"""Angel Enrique Montes Pacheco"""
def randcolor():
    """Select a random color"""
    color = ["green", "blue", "yellow", "purple", "black"]
    return random.choice(color)

"""David Rangel Monsiváis"""
def add_block():
    """Add a block (obstacle) at a random free position."""
    tries = 0
    while True:
        tries += 1
        new_block = vector(randrange(-15, 15) * 10, randrange(-15, 15) * 10)
        conflict = False
        for b in snake + obstacles + [food, boomFood, trashFood]:  # MODIFICADO: considerar comidas bomba
            if new_block.x == b.x and new_block.y == b.y:
                conflict = True
                break
        if not conflict:
            obstacles.append(new_block)
            print(f"[add_block] Añadido bloque en ({new_block.x}, {new_block.y}) después de {tries} intentos")
            break
        if tries > 200:
            print("[add_block] No se encontró posición libre tras 200 intentos. Abortando add_block.")
            break

def _sync_colors():
    """Asegura que snake_colors y snake tengan la misma longitud.
       Si faltan colores, se añaden al final (cabeza). Si sobran, se recortan (se mantienen los últimos)."""
    if len(snake_colors) < len(snake):
        for _ in range(len(snake) - len(snake_colors)):
            snake_colors.append(randcolor())
        print(f"[sync] Se añadieron {len(snake) - len(snake_colors)} colores (ahora {len(snake_colors)})")
    elif len(snake_colors) > len(snake):
        # conservar los últimos colores (alinear con la cabeza)
        extra = len(snake_colors) - len(snake)
        del snake_colors[0:extra]
        print(f"[sync] Se eliminaron {extra} colores sobrantes (ahora {len(snake_colors)})")

"""Modificado para add_block, multicolor y comidas especiales"""
def move():
    """Move snake forward one segment."""
    global timeDelay, special_food, cpu_active
    try:
        head = snake[-1].copy()
        head.move(aim)

        # choque con paredes, cuerpo u obstáculo
        if not inside(head) or head in snake or head in obstacles or head in cpu_snake:
            square(head.x, head.y, 9, 'red')
            update()
            return

        snake.append(head)

        # --- lógica de comida normal y special_food ---
        if head == food:
            # mover comida a nueva posición libre
            
            # Activa la serpiente CPU
            if len(snake) - 1 >= spawn_score and not cpu_active:
                cpu_active = True
                cpu_snake.append(vector(-100, 0))

            tries = 0
            while True:
                tries += 1
                new_fx = randrange(-15, 15) * 10
                new_fy = randrange(-15, 15) * 10
                conflict = False
                for b in snake + obstacles + [boomFood, trashFood]:  # MODIFICADO: evitar comidas bomba
                    if new_fx == b.x and new_fy == b.y:
                        conflict = True
                        break
                if not conflict:
                    food.x = new_fx
                    food.y = new_fy
                    break
                if tries > 500:
                    break

            # decidir si la comida es especial
            if random.random() < 0.2:
                special_food = True
            else:
                special_food = False

            if special_food:
                for _ in range(3):  # crecer 3 bloques
                    snake_colors.append(randcolor())
            else:
                snake_colors.append(randcolor())

            special_food = False  # resetear bandera

            add_block()  # agregar obstáculo

            # acelerar serpiente
            prev = timeDelay
            if timeDelay > minTimeDelay:
                timeDelay = max(minTimeDelay, timeDelay - timeDecrement)

        # --- lógica de comidas bomba ---
        elif head == boomFood:
            if len(snake) > 3:
                del snake[-4:]
            else:
                square(head.x, head.y, 9, "orange")
                update()
                return
            # mover boomFood a nueva posición
            while True:
                new_bx = randrange(-15, 15) * 10
                new_by = randrange(-15, 15) * 10
                if (new_bx, new_by) not in [(s.x, s.y) for s in snake] + [(food.x, food.y), (trashFood.x, trashFood.y)]:
                    boomFood.x = new_bx
                    boomFood.y = new_by
                    break

        elif head == trashFood:
            if len(snake) > 2:
                del snake[-2:]
            else:
                square(head.x, head.y, 9, "red")
                update()
                return
            # mover trashFood a nueva posición
            while True:
                new_tx = randrange(-15, 15) * 10
                new_ty = randrange(-15, 15) * 10
                if (new_tx, new_ty) not in [(s.x, s.y) for s in snake] + [(food.x, food.y), (boomFood.x, boomFood.y)]:
                    trashFood.x = new_tx
                    trashFood.y = new_ty
                    break

        else:
            # si no comió: quitar cola
            if len(snake) > 1:
                snake.pop(0)
            if len(snake_colors) > 1:
                snake_colors.pop(0)

        _sync_colors()

        # --- dibujar todo ---
        clear()
        for body, color_seg in zip(snake, snake_colors):
            square(body.x, body.y, 9, color_seg)

        # comida normal / special_food
        if special_food:
            square(food.x, food.y, 9, randcolor())
        else:
            square(food.x, food.y, 9, 'green')

        #serpiente cpu
        if cpu_active:
                move_cpu()
                for body in cpu_snake:
                    square(body.x, body.y, 9, 'blue')

        # comidas bomba
        square(boomFood.x, boomFood.y, 9, 'black')
        square(trashFood.x, trashFood.y, 9, 'red')

        # obstáculos
        for block in obstacles:
            square(block.x, block.y, 9, 'red')

        update()

    finally:
        ontimer(move, int(timeDelay))

"""Carlos Arias Capetillo"""
# Configuración de velocidad
timeDelay = 250      # tiempo inicial
timeDecrement = 15   # decremento en cada comida
minTimeDelay = 50    # límite mínimo

"""Carlos Almaraz Arrambide"""
def foodmove():
    """Move food randomly within boundaries."""
    global fooddir
    try:
        if random.random() < 0.2:
            fooddir = choice([vector(10,0), vector(-10,0), vector(0,10), vector(0,-10)])
        next_food = food + fooddir
        if inside(next_food):
            food.move(fooddir)
        else:
            fooddir = choice([vector(10,0), vector(-10,0), vector(0,10), vector(0,-10)])
    finally:
        ontimer(foodmove, int(foodspeed))

# --- Main ---
setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
onkey(lambda: change(10, 0), 'Right')
onkey(lambda: change(-10, 0), 'Left')
onkey(lambda: change(0, 10), 'Up')
onkey(lambda: change(0, -10), 'Down')

# iniciar loops
foodmove()
move()
done()