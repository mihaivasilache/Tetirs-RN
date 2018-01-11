import sys
import time

from shapes import *
from network import *
import numpy as np

DISPLAY = True
SAVE_FILE = 'data3/h24-'


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

    current_epsilon = -1
    current_learning_rate = -1
    file_name = 1
    need_new_piece = False
    score = 0
    total_score = 0
    move_loss = 0.01
    move_win = 2500
    line_good_score = 1
    max_height = 2
    stay_alive = 0
    game_over = False
    last_levels = 2

    agent = Network(last_levels * BOARD_WIDTH + 4, 4)
    agent.load_model(SAVE_FILE)
    max_score = -9999999999

    while True:
        if piece is None:
            piece = get_new_piece()

        if not is_valid_position(board, piece):
            if file_name % 1 == 0:
                print('Iteration: ' + str(file_name) + ' Score: ' + str(total_score) + ' Epsilon: ' + str(agent.epsilon))
            game_over = True
            max_score += total_score
            score -= 100

            agent.remember(state, action, score, next_state, game_over)
            agent.replay(32)
            max_height = 2

            if file_name % 250 == 0:
                print('Saving model.')
                agent.save_model(SAVE_FILE + str(file_name) + ' - ' + str(max_score/250))

            max_score = 0

            total_score = 0

            file_name += 1
            board = get_blank_board()
            need_new_piece = False
            score = 0
            piece = get_new_piece()
            game_over = False
            screen, clock = initialise()

        # print(get_top_levels(board, 2))
        # print(get_top_levels(board, 2) + [piece['x'], piece['y'], ord(piece['shape']), piece['rotation']])
        state = np.array(get_top_levels(board, last_levels) + [piece['x'], BOARD_HEIGHT - last_levels - piece['y'],
                                                               piece['rotation'], SHAPES_INDEX[piece['shape']]])
        state = state.reshape(1, last_levels*BOARD_WIDTH + 4)
        action = agent.act(state)
        # print(action)

        # print(state.shape)
        # for event in pygame.event.get():
        # if action == 0:
        #     pass
        # elif event.key == K_SPACE and event.type == pygame.KEYDOWN:
        if action == 0:
            score -= move_loss
            pass
        if action == 1:
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
                        # screen, clock = initialise()
                if event.key == pygame.K_SPACE:
                    if agent.epsilon != 0:
                        current_epsilon = agent.epsilon
                        current_learning_rate = agent.learning_rate
                        agent.epsilon = 0
                        agent.learning_rate = 0
                    else:
                        agent.epsilon = current_epsilon
                        agent.learning_rate = current_learning_rate

        sleep = False
        piece['y'] += 1
        if not is_valid_position(board, piece):
            piece['y'] -= 1
            # lines_score = get_board_score(board, piece)
            line_score = 0
            add_to_board(board, piece)
            if max_height < get_height(board):
                score -= 25
                max_height = get_height(board)
            lines_completed = remove_complete_lines(board)
            score += lines_completed * move_win
            need_new_piece = True
            # print('ls:', lines_score)
            sleep = False

        if DISPLAY:
            screen.fill(BG_COLOR)
            draw_board(screen, board)

            if piece is not None:
                draw_piece(screen, piece)

        if DISPLAY:
            pygame.display.update()
            clock.tick(FPS)

        if sleep:
            time.sleep(10)

        if speed != 0:
            time.sleep(speed)

        next_state = np.array(get_top_levels(board, last_levels) + [piece['x'], BOARD_HEIGHT - last_levels - piece['y'],
                                                                    piece['rotation'], SHAPES_INDEX[piece['shape']]])

        next_state = next_state.reshape(1, last_levels * BOARD_WIDTH + 4)

        if game_over is not False:
            score += stay_alive

        score += get_constant_score(board, piece)

        agent.remember(state, action, score, next_state, game_over)

        total_score += score
        # print('score ', score)
        score = 0

        # print(score)

        if need_new_piece:
            piece = get_new_piece()
            need_new_piece = False
            score = 0

        # time.sleep(0.2)

        # print(score)


def main():
    global SAVE_FILE

    if len(sys.argv) > 1:
        SAVE_FILE = sys.argv[1]

    screen, clock = initialise()
    start_game(screen, clock, 0)


if __name__ == "__main__":
    main()
