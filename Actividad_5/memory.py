"""Memory, puzzle game of number pairs.

Exercises:

1. Count and print how many taps occur.
2. Decrease the number of tiles to a 4x4 grid.
3. Detect when all tiles are revealed.
4. Center single-digit tile.
5. Use letters instead of tiles.
"""

from random import *
from turtle import *

from freegames import path

car = path('car.gif')
tiles = ['🍎','🍌','🍇','🍉','🍓','🍒','🥝','🍑',
         '🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼',
         '🚗','🚲','🚀','🚂','🛵','✈️','🚁','🚤',
         '⚽','🏀','🏈','🎾','🎲','🎮','🎹','🎸'] * 2 #Cambiar de números  a objetos (David Rangel Monsiváis)

state = {'mark': None}
hide = [True] * 64


def square(x, y):
    """Draw white square with black outline at (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(50)
        left(90)
    end_fill()


def index(x, y):
    """Convert (x, y) coordinates to tiles index."""
    return int((x + 200) // 50 + ((y + 200) // 50) * 8)


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 8) * 50 - 200, (count // 8) * 50 - 200


def tap(x, y):
    """Update mark and hidden tiles based on tap."""
    spot = index(x, y)
    mark = state['mark']

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None


def draw():
    """Draw image and tiles."""
    clear()
    goto(0, 0)
    shape(car)
    stamp()

    for count in range(64):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()

        # Diccionario de ajustes verticales por emoji
        emoji_fix = {
            '✈️': -5,
            '🚁': -5,
            '🚀': -3,
            '🚂': -2,
        }

        # Obtiene el ajuste si existe, sino 0
        dy = emoji_fix.get(tiles[mark], 0)

        goto(x + 25, y + 5 + dy)   # centrado horizontal y corregido vertical (David Rangel Monsiváis)
        color('black')
        write(tiles[mark], align='center', font=('Segoe UI Emoji', 22, 'normal'))

    update()
    ontimer(draw, 100)




shuffle(tiles)
setup(420, 420, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()