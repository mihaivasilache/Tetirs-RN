import sys
import time

from pygame.locals import *
from shapes import *


DISPLAY = True


def initialise():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return screen, clock


def start_game(screen, clock, speed):
    global DISPLAY
    board = get_blank_board()
    print(len(board), len(board[0]))
    piece = get_new_piece()
    need_new_piece = False
    score = 0
    move_loss = 10
    move_win = 1000
    start_time = time.time()
    game_over = False

    while True:
        if piece is None:
            piece = get_new_piece()

        if not is_valid_position(board, piece):
            game_over = True
            return

        for event in pygame.event.get():
            if not hasattr(event, 'key'):
                continue
            elif event.key == K_SPACE and event.type == pygame.KEYDOWN:
                piece['rotation'] = (piece['rotation'] - 1) % len(SHAPES[piece['shape']])
                score -= move_loss
                if not is_valid_position(board, piece):
                    piece['rotation'] = (piece['rotation'] + 1) % len(SHAPES[piece['shape']])
                    score += move_loss
            elif event.key == K_LEFT and event.type == pygame.KEYDOWN:
                piece['x'] -= 1
                score -= move_loss
                if not is_valid_position(board, piece):
                    piece['x'] += 1
                    score += move_loss
            elif event.key == K_RIGHT and event.type == pygame.KEYDOWN:
                piece['x'] += 1
                score -= move_loss
                if not is_valid_position(board, piece):
                    piece['x'] -= 1
                    score += move_loss
            elif event.key == K_ESCAPE:
                sys.exit(0)

        piece['y'] += 1
        if not is_valid_position(board, piece):
            piece['y'] -= 1
            add_to_board(board, piece)
            score += remove_complete_lines(board)*move_win
            need_new_piece = True

        if DISPLAY:
            screen.fill(BG_COLOR)
            draw_board(screen, board)

        if piece is not None:
            draw_piece(screen, piece)
        if need_new_piece:
            piece = get_new_piece()
            need_new_piece = False

        if DISPLAY:
            pygame.display.update()
            clock.tick(FPS)

        if time.time() - start_time > 5:
            DISPLAY = True

        if speed != 0:
            time.sleep(speed)

        print(score)


def main():
    screen, clock = initialise()
    start_game(screen, clock, 0.35)


if __name__ == "__main__":
    main()
