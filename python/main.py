import random
import math
import time
import os
import keyboard

gamewindow = []
snake = []

score = 0

width = 50
height = 20

sx = math.ceil(width / 3)
sy = math.ceil(height / 2)

ax = 0
ay = 0

skip_snake_growth = False

current_dir = "right"
next_dir = "right"
opposites = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}

def random_apple():
    global gamewindow, ax, ay
    
    ax = random.randint(1, width-2)
    ay = random.randint(1, height-2)

    while (ax, ay) in snake:
        ax = random.randint(1, width-2)
        ay = random.randint(1, height-2)

def init_snake():
    global snake
    snake.append((math.floor(width / 2), math.floor(height / 2)))

def move_snake():
    global snake, skip_snake_growth, current_dir, next_dir

    if len(snake) == 0:
        return

    if not (len(snake) > 1 and next_dir == opposites[current_dir]):
        current_dir = next_dir

    dir = current_dir

    head_x, head_y = snake[0]

    if dir == "up":
        new_head = (head_x, head_y - 1)
    elif dir == "down":
        new_head = (head_x, head_y + 1)
    elif dir == "left":
        new_head = (head_x - 1, head_y)
    else:
        new_head = (head_x + 1, head_y)
    
    if new_head in snake:
        print("Game Over")
        exit()

    # boundary check (IMPORTANT)
    if (
        new_head[0] <= 0 or new_head[0] >= width - 1 or
        new_head[1] <= 0 or new_head[1] >= height - 1
    ):
        print("Game Over")
        exit()
    
    if new_head[0] == ax and new_head[1] == ay:
        apple_eaten()

    # move snake
    snake.insert(0, new_head)

    if not skip_snake_growth:
        if len(snake) > 1:
            snake.pop()
    else:
        skip_snake_growth = False
    
    if len(snake) != len(set(snake)):
        print("Game Over")
        exit()
    
    if dir == "up" or dir == "down":
        time.sleep(0.5/10)

def apple_eaten():
    global score, skip_snake_growth
    score += 100
    skip_snake_growth = True
    random_apple()

def init_borders():
    global gamewindow
    temp = []
    for row in range(height):
        new_row = []
        for cell in range(width):
            if (row == 0 or row == height - 1) or (cell == 0 or cell == width - 1):
                new_row.append("█")
            else:
                new_row.append(" ")
        temp.append(new_row)
    return temp

def check_keyboard_input():
    global next_dir
    if keyboard.is_pressed("up"):
        next_dir = "up"
    elif keyboard.is_pressed("down"):
        next_dir = "down"
    elif keyboard.is_pressed("left"):
        next_dir = "left"
    elif keyboard.is_pressed("right"): # assume right as always
        next_dir = "right"

def frame():
    global gamewindow, score, snake
    
    print("\x1b[1;1H", end="")
    
    for cy in range(len(gamewindow)):
        for cx in range(len(gamewindow[cy])):
            print(gamewindow[cy][cx], end="")
        print()
    
    scoretxt = f"Score: {score}"
    gamewindow = init_borders()
    
    for x, y in snake:
        if snake[0] == (x, y):
            gamewindow[y][x] = "@"
        else:
            gamewindow[y][x] = "#"

    for length in range(len(scoretxt)):
        gamewindow[0][length] = scoretxt[length]
    
    gamewindow[ay][ax] = "$"
    
def main_loop():
    global score
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        time.sleep(1/10)
        frame()
        check_keyboard_input()
        move_snake()
        frame()

init_snake()
random_apple()
main_loop()
