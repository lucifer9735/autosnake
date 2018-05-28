import curses
from random import randint

HEIGHT = 10
WIDTH = 20
FIELD_SIZE = HEIGHT * WIDTH

SPEED = 300
food = 3 * WIDTH + 3
key = 1 
score = 1

HEAD = 0

FOOD = 0
UNDEFINED = (HEIGHT +1) * (WIDTH + 1)
SNAKE = 2 * UNDEFINED

h = 104
j = 106
k = 107
l = 108
LEFT = -1
RIGHT = 1
UP = -WIDTH
DOWN = WIDTH
mov = [LEFT, RIGHT, UP, DOWN]

ERR = -1111

board = [0] * FIELD_SIZE
snake = [0] * (FIELD_SIZE + 1)
snake[HEAD] = 1*WIDTH + 1
snake_size = 1

def shift_array(arr, size):
    for i in range(size, 0, -1):
        arr[i] = arr[i-1]

def is_cell_free(idx, psnake, psize):
    return not(idx in psnake[:psize])

def new_food():
    global food, snake_size
    cell_free = False
    while not cell_free:
        w = randint(1, WIDTH-2)
        h = randint(1, HEIGHT-2)
        food = h*WIDTH + w
        cell_free = is_cell_free(food, snake, snake_size)
    win.addch(food//WIDTH, food%WIDTH, '@')

def make_move(pbest_move):
    global key, board, snake, snake_size, score
    shift_array(snake, snake_size)
    snake[HEAD] += pbest_move

    p = snake[HEAD]
    win.addch(p//WIDTH, p%WIDTH, '*')

    if snake[HEAD] == food:
        board[snake[HEAD]] = SNAKE
        snake_size += 1
        score += 1
        if snake_size < FIELD_SIZE: new_food()
    else:
        board[snake[HEAD]] = SNAKE
        board[snake[snake_size]] = UNDEFINED
        win.addch(snake[snake_size]//WIDTH, snake[snake_size]%WIDTH, ' ')


curses.initscr()
win = curses.newwin(HEIGHT, WIDTH, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
win.addch(food//WIDTH, food%WIDTH, '@')


event = 0
while event != 27:
    win.addstr(0, 2, ' S:' + str(score) + ' ')
    win.timeout(SPEED)
    event = win.getch()
    if event != -1:
        if event == 27:break
        elif event == h:
            key = key if key == RIGHT else LEFT
        elif event == l:
            key = key if key == LEFT else RIGHT
        elif event == j:
            key = key if key == UP else DOWN
        elif event == k:
            key = key if key == DOWN else UP
    make_move(key)

win.keypad(0)
curses.echo()
curses.endwin()
