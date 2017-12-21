import sys
import time

from pygame.locals import *
from shapes import *


def initialise():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return screen, clock


def start_game(screen, clock):
    board = get_blank_board()
    piece = get_new_piece()
    need_new_piece = False
    score = 0

    while True:
        if piece is None:
            piece = get_new_piece()

        if not is_valid_position(board, piece):
            return

        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            elif event.key == K_SPACE and event.type == pygame.KEYDOWN:
                piece['rotation'] = (piece['rotation'] - 1) % len(SHAPES[piece['shape']])
                if not is_valid_position(board, piece):
                    piece['rotation'] = (piece['rotation'] + 1) % len(SHAPES[piece['shape']])
            elif event.key == K_LEFT and event.type == pygame.KEYDOWN:
                piece['x'] -= 1
                if not is_valid_position(board, piece):
                    piece['x'] += 1
            elif event.key == K_RIGHT and event.type == pygame.KEYDOWN:
                piece['x'] += 1
                if not is_valid_position(board, piece):
                    piece['x'] -= 1
            elif event.key == K_ESCAPE:
                sys.exit(0)

        piece['y'] += 1
        if not is_valid_position(board, piece):
            piece['y'] -= 1
            add_to_board(board, piece)
            score += remove_complete_lines(board)
            need_new_piece = True

        screen.fill(BG_COLOR)
        draw_board(screen, board)
        if piece is not None:
            draw_piece(screen, piece)
        if need_new_piece:
            piece = get_new_piece()
            need_new_piece = False

        pygame.display.update()
        clock.tick(FPS)

        time.sleep(0.25)

        print(score)


def main():
    screen, clock = initialise()
    start_game(screen, clock)


if __name__ == "__main__":
    main()
