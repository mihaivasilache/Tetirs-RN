import time

from shapes import *
from network import *
import numpy as np

DISPLAY = True


def initialise():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    return screen, clock


def start_game(screen, clock, speed):
    file_name = 1
    global DISPLAY
    board = get_blank_board()
    piece = get_new_piece()
    need_new_piece = False
    score = 0
    move_loss = 10
    move_win = 1000
    stay_alive = 5
    start_time = time.time()
    game_over = False

    agent = Network(BOARD_HEIGHT*BOARD_WIDTH, 4)

    while True:
        if piece is None:
            piece = get_new_piece()

        if not is_valid_position(board, piece):
            game_over = True
            agent.remember(state, action, score, next_state, game_over)
            agent.replay(32)
            if file_name % 20 == 0:
                agent.save_weights('neural/'+file_name)
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
        # elif event.key == K_ESCAPE:
        #     sys.exit(0)

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

        if time.time() - start_time > 0:
            DISPLAY = True

        if speed != 0:
            time.sleep(speed)

        next_state = np.array([i for j in board for i in j])
        next_state = next_state.reshape(1, 200)

        if game_over is not False:
            score += stay_alive
        agent.remember(state, action, score, next_state, game_over)

        # print(score)


def main():
    screen, clock = initialise()
    start_game(screen, clock, 0)


if __name__ == "__main__":
    main()
