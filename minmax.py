import math
import random

from game import Game

EMPTY = 0
PLAYER_1_PIECE = 1
PLAYER_2_PIECE = 2
WINDOW_LENGTH = 4
N_COLS = 7
N_ROWS = 6


class Minmax:

    def __init__(self):
        self.game = Game()

    # calculate the values of a window
    def evaluate_window(self, window, piece):
        score = 0
        opponent_piece = PLAYER_1_PIECE
        if piece == PLAYER_1_PIECE:
            opponent_piece = PLAYER_2_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
        if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    # assign a score
    def score_position(self, board, piece):
        score = 0
        center_array = [int(i) for i in list(board[:, N_COLS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # horiz score
        for r in range(N_ROWS):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(N_COLS - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # vertical score
        for c in range(N_COLS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(N_ROWS - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        # positive diag
        for r in range(N_ROWS - 3):
            for c in range(N_COLS - 3):
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        # negative diag
        for r in range(N_ROWS - 3):
            for c in range(N_COLS - 3):
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score


    def is_terminal_node(self, board):
        return self.game.winning_move(board, PLAYER_1_PIECE) or self.game.winning_move(board, PLAYER_2_PIECE) or len(self.game.get_valid_locations(board)) == 0

    #minmax algorithm
    def minmax(self, board, depth, maxPlayer):
        valid_locations = self.game.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.game.winning_move(board, PLAYER_2_PIECE):
                    return None, 100000
                elif self.game.winning_move(board, PLAYER_1_PIECE):
                    return None, -100000
                else:  # game over
                    return None, 0
            else:  # depth 0
                return None, self.score_position(board, PLAYER_2_PIECE)

        if maxPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                self.game.drop(b_copy, col, PLAYER_2_PIECE)
                new_score = self.minmax(b_copy, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value

        else:  # minplayer
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                b_copy = board.copy()
                self.game.drop(b_copy, col, PLAYER_1_PIECE)
                new_score = self.minmax(b_copy, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value