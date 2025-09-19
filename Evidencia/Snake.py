"""Snake, classic arcade game.

Extras implementados:
1. La comida se mueve aleatoriamente.
2. Cada que la serpiente come, aparece un bloque obstáculo.
3. La serpiente es multicolor (cada segmento conserva su color).
4. La serpiente acelera cada que come.
"""

import random
from random import randrange, choice
from turtle import *
from freegames import square, vector

# --- Estado del juego ---
food = vector(0, 0)
snake = [vector(10, 0)]
snake_colors = ["green"]  # lista paralela: color de cada segmento (misma longitud que `snake`)
aim = vector(0, -10)
fooddir = vector(10, 0)
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
        for b in snake + obstacles + [food]:
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

"""Modificado para add_block y multicolor"""
def move():
    """Move snake forward one segment."""
    global timeDelay
    try:
        # debug
        print(f"[move] ENTER timeDelay={timeDelay} snake_len={len(snake)} colors_len={len(snake_colors)} obstacles={len(obstacles)}")

        head = snake[-1].copy()
        head.move(aim)

        # choque con paredes, cuerpo u obstáculo
        if not inside(head) or head in snake or head in obstacles:
            square(head.x, head.y, 9, 'red')
            update()
            print("[move] FIN: choque detectado. Juego terminado en esta ejecución de move().")
            return

        snake.append(head)

        if head == food:
            print('Snake:', len(snake))
            # mover comida a nueva posición libre (evitar ponerla encima de snake u obstáculos)
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
                    print("[move] No se encontró posición libre para la comida tras 500 intentos.")
                    break

            # nuevo color para el segmento añadido (la cabeza que se añadió)
            snake_colors.append(randcolor())

            # añadir obstáculo
            add_block()

            # acelerar la serpiente
            prev = timeDelay
            if timeDelay > minTimeDelay:  # Carlos Arias Capetillo
                timeDelay = max(minTimeDelay, timeDelay - timeDecrement)
            print(f"[move] Comer detectado: timeDelay {prev} -> {timeDelay}")
        else:
            # si no comió: quitar cola tanto en snake como en colores
            if len(snake) > 1:
                snake.pop(0)
            if len(snake_colors) > 1:
                snake_colors.pop(0)

        # sincronizar por si acaso
        if len(snake_colors) != len(snake):
            # preferimos arreglar sin cambiar colores existentes salvo cuando haga falta
            if len(snake_colors) < len(snake):
                # si faltan, agregar colores al final (para las nuevas cabezas)
                for _ in range(len(snake) - len(snake_colors)):
                    snake_colors.append(randcolor())
                print(f"[move-sync] Agregados colores, ahora {len(snake_colors)}")
            else:
                # recortar los extras (mantener los últimos)
                extra = len(snake_colors) - len(snake)
                del snake_colors[0:extra]
                print(f"[move-sync] Recortados {extra} colores, ahora {len(snake_colors)}")

        clear()

        # dibujar serpiente multicolor
        for body, color_seg in zip(snake, snake_colors):
            square(body.x, body.y, 9, color_seg)

        # dibujar comida
        square(food.x, food.y, 9, 'green')

        # dibujar obstáculos
        for block in obstacles:
            square(block.x, block.y, 9, 'red')

        update()
    except Exception as e:
        print("[move] Exception:", type(e).__name__, e)
    finally:
        # siempre reprogramar el siguiente movimiento (con timeDelay actual)
        try:
            ontimer(move, int(timeDelay))
        except Exception as e:
            print("[move] Error al programar ontimer:", type(e).__name__, e)

"""Carlos Arias Capetillo"""
# Configuración de velocidad
timeDelay = 250      # tiempo inicial (más lento)
timeDecrement = 15   # decremento en cada comida
minTimeDelay = 50    # límite mínimo

"""Carlos Almaraz Arrambide"""
def foodmove():
    """Move food randomly within boundaries."""
    global fooddir
    try:
        # posibilidad de cambiar dirección
        if random.random() < 0.2:
            fooddir = choice([vector(10, 0), vector(-10, 0), vector(0, 10), vector(0, -10)])
        next_food = food + fooddir
        if inside(next_food):
            food.move(fooddir)
        else:
            fooddir = choice([vector(10, 0), vector(-10, 0), vector(0, 10), vector(0, -10)])
        # debug
        print(f"[foodmove] food at ({food.x}, {food.y}) dir=({fooddir.x},{fooddir.y})")
    except Exception as e:
        print("[foodmove] Exception:", type(e).__name__, e)
    finally:
        try:
            ontimer(foodmove, int(foodspeed))
        except Exception as e:
            print("[foodmove] Error al programar ontimer:", type(e).__name__, e)

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
