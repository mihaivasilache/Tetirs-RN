import sys
import time

from shapes import *
from network import *
import numpy as np

DISPLAY = True
SAVE_FILE = 'data/model.h5'


def initialise():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return screen, clock


def start_game(screen, clock, speed):
    global DISPLAY
    global SAVE_FILE

    board = get_blank_board()
    piece = get_new_piece()

    file_name = 1
    need_new_piece = False
    score = 0
    move_loss = 10
    move_win = 5000
    line_good_score = 1
    stay_alive = 5
    start_time = time.time()
    game_over = False

    agent = Network(BOARD_HEIGHT * BOARD_WIDTH, 4)
    agent.load_model(SAVE_FILE)

    while True:
        if piece is None:
            piece = get_new_piece()

        if not is_valid_position(board, piece):
            # print('Score: ' + str(score))
            game_over = True
            agent.remember(state, action, score, next_state, game_over)
            agent.replay(32)

            if file_name % 20 == 0:
                print('Saving model.')
                agent.save_model(SAVE_FILE)

            file_name += 1
            board = get_blank_board()
            need_new_piece = False
            score = 0
            piece = get_new_piece()
            start_time = time.time()
            game_over = False
            screen, clock = initialise()

        state = np.array([i for j in board for i in j])
        state = state.reshape(1, 200)
        action = agent.act(state)

        # print(state.shape)
        # for event in pygame.event.get():
        if action == 0:
            continue
        # elif event.key == K_SPACE and event.type == pygame.KEYDOWN:
        elif action == 1:
            piece['rotation'] = (piece['rotation'] - 1) % len(SHAPES[piece['shape']])
            score -= move_loss
            if not is_valid_position(board, piece):
                piece['rotation'] = (piece['rotation'] + 1) % len(SHAPES[piece['shape']])
                score += move_loss
        # elif event.key == K_LEFT and event.type == pygame.KEYDOWN:
        elif action == 2:
            piece['x'] -= 1
            score -= move_loss
            if not is_valid_position(board, piece):
                piece['x'] += 1
                score += move_loss
        # elif event.key == K_RIGHT and event.type == pygame.KEYDOWN:
        elif action == 3:
            piece['x'] += 1
            score -= move_loss
            if not is_valid_position(board, piece):
                piece['x'] -= 1
                score += move_loss

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if DISPLAY:
                        DISPLAY = False
                    else:
                        DISPLAY = True

        piece['y'] += 1
        if not is_valid_position(board, piece):
            piece['y'] -= 1
            add_to_board(board, piece)
            lines_score = get_board_score(board, piece)
            score += lines_score * line_good_score
            lines_completed = remove_complete_lines(board)
            score += lines_completed * move_win
            need_new_piece = True
            # print('ls:', lines_score)
            # time.sleep(5)

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

        # if time.time() - start_time > 0:
        #     DISPLAY = True

        if speed != 0:
            time.sleep(speed)

        next_state = np.array([i for j in board for i in j])
        next_state = next_state.reshape(1, 200)

        if game_over is not False:
            score += stay_alive

        agent.remember(state, action, score, next_state, game_over)

        # print(score)


def main():
    global SAVE_FILE

    if len(sys.argv) > 1:
        SAVE_FILE = sys.argv[1]

    screen, clock = initialise()
    start_game(screen, clock, 0)


if __name__ == "__main__":
    main()
