import pygame
import random
import math

from copy import deepcopy


WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
BLUE = (0, 0, 155)
WINDOW_WIDTH = 260
WINDOW_HEIGHT = 440
# WINDOW_WIDTH = 500
# WINDOW_HEIGHT = 2014
BOX_SIZE = 20
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLANK = 0
FPS = 60

BORDER_COLOR = BLUE
BG_COLOR = BLACK
TEXT_COLOR = WHITE
TEXT_SHADOW_COLOR = GRAY
COLOR = RED

X_MARGIN = int((WINDOW_WIDTH - BOARD_WIDTH * BOX_SIZE) / 2)
TOP_MARGIN = WINDOW_HEIGHT - (BOARD_HEIGHT * BOX_SIZE) - 5

TEMPLATE_WIDTH = 5
TEMPLATE_HEIGHT = 5

S_SHAPE_TEMPLATE = [[[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 1, 1, 0],
                     [0, 1, 1, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 1, 0],
                     [0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0]]]

Z_SHAPE_TEMPLATE = [[[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 0, 1, 1, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0]]]

I_SHAPE_TEMPLATE = [[[0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [1, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]]]

O_SHAPE_TEMPLATE = [[[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 0, 0, 0, 0]]]

J_SHAPE_TEMPLATE = [[[0, 0, 0, 0, 0],
                     [0, 1, 0, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 1, 1, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 0, 1, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 0, 0, 0, 0]]]

L_SHAPE_TEMPLATE = [[[0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 1, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]]]

T_SHAPE_TEMPLATE = [[[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 1, 1, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 1, 1, 1, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]],
                    [[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 1, 1, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]]]

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
    pygame.draw.rect(screen, COLOR, (pixel_x + 1, pixel_y + 1, BOX_SIZE - 1, BOX_SIZE - 1))


def get_new_piece():
    shape = random.choice(list(SHAPES.keys()))
    new_piece = {'shape': shape,
                 'rotation': random.randint(0, len(SHAPES[shape]) - 1),
                 'x': int(BOARD_WIDTH / 2) - int(TEMPLATE_WIDTH / 2),
                 'y': -2,
                 'color': 1}
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


def get_piece_height(piece_shape):
    height = 0
    first_piece = None
    for y in range(len(piece_shape)):
        for x in range(len(piece_shape[y])):
            if piece_shape[y][x] == 1:
                if first_piece is None:
                    first_piece = y
                height += 1
                break

    return height, first_piece


def get_first_x(piece_shape, y):
    for x in range(0, len(piece_shape[y])):
        if piece_shape[y][x] != BLANK:
            return x


def get_board_score(board, piece):
    line_score = 0

    piece_shape = SHAPES[piece['shape']][piece['rotation']]
    piece_height, first_piece = get_piece_height(piece_shape)

    new_board = deepcopy(board)
    temp_board = get_blank_board()
    add_to_board(new_board, piece)
    add_to_board(temp_board, piece)

    # cea mai mica miscare posibila
    line_score -= (get_lowest_move(board, piece) - piece['y']) ** 2
    # print(line_score)

    # consturirea celei mai bune linii
    for y in range(piece['y'] + first_piece, piece['y'] + first_piece + piece_height):
        completed_blocks = 0
        x_to_remember = -1
        for temp_x in range(BOARD_WIDTH):
            if temp_board[temp_x][y] != BLANK:
                x_to_remember = temp_x
                break

        x = x_to_remember
        while x >= 0 and new_board[x][y] != BLANK:
            completed_blocks += 1
            x -= 1

        x = x_to_remember + 1
        while x < BOARD_WIDTH and new_board[x][y] != BLANK:
            completed_blocks += 1
            x += 1

        line_score += completed_blocks ** 3

    # contacul cu alte piese
    contact = 0
    for y in range(piece['y'] + first_piece, piece['y'] + first_piece + piece_height):
        for temp_x in range(BOARD_WIDTH):
            if temp_board[temp_x][y] != BLANK:
                if temp_x + 1 < BOARD_WIDTH:
                    contact += new_board[temp_x + 1][y] - temp_board[temp_x + 1][y]
                if temp_x - 1 >= 0:
                    contact += new_board[temp_x - 1][y] - temp_board[temp_x - 1][y]
                if y + 1 < BOARD_HEIGHT:
                    contact += new_board[temp_x ][y + 1] - temp_board[temp_x][y + 1]
                if y - 1 >= 0:
                    contact += new_board[temp_x][y - 1] - temp_board[temp_x][y - 1]

    contact = (contact ** 3)
    # print('contact' + str(contact))
    return line_score + contact


def get_lowest_move(board, piece):
    new_piece = deepcopy(piece)
    max_y = -1
    for x in range(BOARD_WIDTH):
        new_piece['y'] = 0
        new_piece['x'] = x
        while is_valid_position(board, new_piece) is True:
            new_piece['y'] += 1
        if new_piece['y'] > max_y:
            max_y = new_piece['y']
    return max_y


if __name__ == "__main__":
    pass
