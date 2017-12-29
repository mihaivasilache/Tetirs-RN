import pygame
import random

WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHT_RED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHT_GREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHT_BLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGHT_YELLOW = (175, 175, 20)
WINDOW_WIDTH = 260
WINDOW_HEIGHT = 440
BOX_SIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLANK = '.'
FPS = 30

BORDER_COLOR = BLUE
BG_COLOR = BLACK
TEXT_COLOR = WHITE
TEXT_SHADOW_COLOR = GRAY
COLORS = (BLUE, GREEN, RED, YELLOW)
LIGHT_COLORS = (LIGHT_BLUE, LIGHT_GREEN, LIGHT_RED, LIGHT_YELLOW)
assert len(COLORS) == len(LIGHT_COLORS)

X_MARGIN = int((WINDOW_WIDTH - BOARD_WIDTH * BOX_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (BOARD_HEIGHT * BOX_SIZE) - 5

TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

SHAPES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def draw_piece(screen, piece, pixel_x=None, pixel_y=None):
    shape_to_draw = SHAPES[piece['shape']][piece['rotation']]
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = convert_to_pixel_cords(piece['x'], piece['y'])

    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if shape_to_draw[y][x] != BLANK:
                draw_box(screen, None, None, piece['color'], pixel_x + (x * BOX_SIZE), pixel_y + (y * BOX_SIZE))


def convert_to_pixel_cords(box_x, box_y):
    return (X_MARGIN + (box_x * BOX_SIZE)), (TOP_MARGIN + (box_y * BOX_SIZE))


def draw_box(screen, box_x, box_y, draw_color, pixel_x=None, pixel_y=None):
    if draw_color == BLANK:
        return
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = convert_to_pixel_cords(box_x, box_y)
    pygame.draw.rect(screen, COLORS[draw_color], (pixel_x + 1, pixel_y + 1, BOX_SIZE - 1, BOX_SIZE - 1))
    pygame.draw.rect(screen, LIGHT_COLORS[draw_color], (pixel_x + 1, pixel_y + 1, BOX_SIZE - 4, BOX_SIZE - 4))


def get_new_piece():
    shape = random.choice(list(SHAPES.keys()))
    new_piece = {'shape': shape,
                 'rotation': random.randint(0, len(SHAPES[shape]) - 1),
                 'x': int(BOARD_WIDTH / 2) - int(TEMPLATE_WIDTH / 2),
                 'y': -2,
                 'color': random.randint(0, len(COLORS)-1)}
    return new_piece


def is_valid_position(board, piece, adj_x=0, adj_y=0):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            is_above_board = y + piece['y'] + adj_y < 0
            if is_above_board or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not is_on_board(x + piece['x'] + adj_x, y + piece['y'] + adj_y):
                return False
            if board[x + piece['x'] + adj_x][y + piece['y'] + adj_y] != BLANK:
                return False
    return True


def is_on_board(x, y):
    return 0 <= x < BOARD_WIDTH and y < BOARD_HEIGHT


def get_blank_board():
    board = []
    for i in range(BOARD_WIDTH):
        board.append([BLANK] * BOARD_HEIGHT)
    return board


def draw_board(screen, board):
    pygame.draw.rect(screen, BORDER_COLOR, (X_MARGIN - 3, TOP_MARGIN - 7, (BOARD_WIDTH * BOX_SIZE) + 8,
                                            (BOARD_HEIGHT * BOX_SIZE) + 8), 5)

    pygame.draw.rect(screen, BG_COLOR, (X_MARGIN, TOP_MARGIN, BOX_SIZE * BOARD_WIDTH, BOX_SIZE * BOARD_HEIGHT))
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            draw_box(screen, x, y, board[x][y])


def add_to_board(board, piece):
    for x in range(TEMPLATE_WIDTH):
        for y in range(TEMPLATE_HEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def is_complete_line(board, y):
    for x in range(BOARD_WIDTH):
        if board[x][y] == BLANK:
            return False
    return True


def remove_complete_lines(board):
    num_lines_removed = 0
    y = BOARD_HEIGHT - 1
    while y >= 0:
        if is_complete_line(board, y):
            for pullDownY in range(y, 0, -1):
                for x in range(BOARD_WIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            for x in range(BOARD_WIDTH):
                board[x][0] = BLANK
            num_lines_removed += 1
        else:
            y -= 1
    return num_lines_removed


if __name__ == "__main__":
    pass
