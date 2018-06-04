import curses
import time
from random import randint

HEIGHT = 15
WIDTH = 30
FIELD_SIZE = HEIGHT * WIDTH

SPEED = 10
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

tmpboard = [0] * FIELD_SIZE
tmpsnake = [0] * (FIELD_SIZE + 1)
tmpsnake[HEAD] = 1*WIDTH + 1
tmpsnake_size = 1

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
    win.addch(food//WIDTH, food%WIDTH, '$')

def make_move(pbest_move):
    global key, board, snake, snake_size, score
    shift_array(snake, snake_size)
    snake[HEAD] += pbest_move

    p = snake[HEAD]
    win.addch(p//WIDTH, p%WIDTH, '@')

    if snake[HEAD] == food:
        board[snake[HEAD]] = SNAKE
        snake_size += 1
        score += 1
        if snake_size < FIELD_SIZE: new_food()
    else:
        board[snake[HEAD]] = SNAKE
        board[snake[snake_size]] = UNDEFINED
        win.addch(snake[snake_size]//WIDTH, snake[snake_size]%WIDTH, ' ')

# autosnake
def is_movable(idx, move):
    flag = False
    if move == LEFT:
        flag = True if idx%WIDTH > 1 else False
    elif move == RIGHT:
        flag = True if idx%WIDTH < (WIDTH-2) else False
    elif move == UP:
        flag = True if idx//WIDTH > 1 else False
    elif move == DOWN:
        flag = True if idx//WIDTH < (HEIGHT-2) else False
    return flag

def board_reset(pboard, psnake, psize):
    for i in range(FIELD_SIZE):
        if i == food:
            pboard[i] = FOOD
        elif is_cell_free(i, psnake, psize):
            pboard[i] = UNDEFINED
        else:
            pboard[i] = SNAKE

def board_scan(pboard, psnake, pfood):
    queue = []
    queue.append(pfood)
    inqueue = [0] * FIELD_SIZE
    found = False
    while len(queue) != 0:
        idx = queue.pop(0)
        if inqueue[idx] == 1: continue
        inqueue[idx] = 1
        for i in range(4):
            if is_movable(idx, mov[i]):
                pidx = idx + mov[i]
                if pidx == psnake[HEAD]:
                    found = True
                elif pboard[pidx] < SNAKE:
                    if pboard[pidx] > pboard[idx]+1:
                        pboard[pidx] = pboard[idx] + 1
                    if inqueue[pidx] == 0:
                        queue.append(pidx)
    return found

def choose_shortest(pboard, psnake):
    best_move = ERR
    min = SNAKE
    for i in range(4):
        pidx = psnake[HEAD] + mov[i]
        if is_movable(psnake[HEAD], mov[i]) and pboard[pidx]<min:
            min = pboard[pidx]
            best_move = mov[i]
    return best_move

def choose_longest(pboard, psnake):
    best_move = ERR
    max = -1
    for i in range(4):
        pidx = psnake[HEAD] + mov[i]
        if is_movable(psnake[HEAD], mov[i]) and pboard[pidx]<UNDEFINED and pboard[pidx]>max:
            max = pboard[pidx]
            best_move = mov[i]
    return best_move

def follow_tail():
    global tmpboard, tmpsnake, tmpsnake_size, food
    tmpsnake_size = snake_size
    tmpsnake = snake[:]
    board_reset(tmpboard, tmpsnake, tmpsnake_size)
    tmpboard[tmpsnake[tmpsnake_size-1]] = FOOD
    tmpboard[food] = SNAKE
    board_scan(tmpboard, tmpsnake, tmpsnake[tmpsnake_size-1])
    tmpboard[tmpsnake[tmpsnake_size-1]] = SNAKE
    return choose_longest(tmpboard, tmpsnake)

def wander():
    best_move = ERR
    for i in range(4):
        idx = snake[HEAD] + mov[i]
        if is_movable(snake[HEAD], mov[i]) and board[idx]<SNAKE:
            return mov[i]

def virtual_move():
    global board, snake, snake_size, tmpboard, tmpsnake, tmpsnake_size, food
    tmpboard = board[:]
    tmpsnake = snake[:]
    tmpsnake_size = snake_size
    board_reset(tmpboard, tmpsnake, tmpsnake_size)

    food_eaten = False
    while not food_eaten:
        board_scan(tmpboard, tmpsnake, food)
        tmpmove = choose_shortest(tmpboard, tmpsnake)
        shift_array(tmpsnake, tmpsnake_size)
        tmpsnake[HEAD] += tmpmove
        if tmpsnake[HEAD] == food:
            tmpsnake_size += 1
            board_reset(tmpboard, tmpsnake, tmpsnake_size)
            tmpboard[food] = SNAKE
            food_eaten = True
        else:
            tmpboard[tmpsnake[HEAD]] = SNAKE
            tmpboard[tmpsnake[tmpsnake_size]] = UNDEFINED

def is_tail_available():
    global tmpboard, tmpsnake, tmpsnake_size, food
    tmpboard[tmpsnake[tmpsnake_size-1]] = 0
    tmpboard[food] = SNAKE
    result = board_scan(tmpboard, tmpsnake, tmpsnake[tmpsnake_size-1])
    return result

def find_safe_way():
    global board, snake
    safe_move = ERR
    virtual_move()
    if is_tail_available():
        return choose_shortest(board, snake)
    safe_move = follow_tail()
    return safe_move

curses.initscr()
win = curses.newwin(HEIGHT, WIDTH, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
win.addch(food//WIDTH, food%WIDTH, '$')


event = 0
while event != 27:
    win.addstr(0, 2, ' S:' + str(score) + ' ')
    win.timeout(SPEED)
    event = win.getch()
    if event == 32: time.sleep(1)
#    if event != -1:
#        if event == 27:break
#        elif event == h:
#            key = key if key == RIGHT else LEFT
#        elif event == l:
#            key = key if key == LEFT else RIGHT
#        elif event == j:
#            key = key if key == UP else DOWN
#        elif event == k:
#            key = key if key == DOWN else UP
#    make_move(key)
    board_reset(board, snake, snake_size)
    if board_scan(board, snake, food):
        best_move = find_safe_way()
    else:
        best_move = follow_tail()

    if best_move != ERR: make_move(best_move)
    else: make_move(wander())

win.keypad(0)
curses.echo()
curses.endwin()
