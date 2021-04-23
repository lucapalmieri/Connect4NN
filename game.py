import numpy as np
import copy

EMPTY = 0
N_ROWS = 6
N_COLS = 7


class Game:

    def __init__(self):
        self.create_board()


    def create_board(self):
        board = np.zeros((N_ROWS, N_COLS))
        self.create_board_history()
        return board


    def create_board_history(self):
        self.board_history = []


    def get_board_history(self):
        return self.board_history


    def print_board(self, board):
        board = np.flip(board, 0) #for graphic purposes, because of the construction of the board = np.zeros, piece will drop on first row and not in the bottom
        str_board = str(board).replace("0.", "_").replace("[", " ").replace("]", " ").replace("1.", "X").replace("2.", "O")
        print("\n  0 1 2 3 4 5 6")
        print(str_board)

    # drop piece in the board, in the row-col position and put the state of the board in the board history
    def drop(self, board, col, piece):
        board[self.get_next_open_row(board, col)][col] = piece
        self.add_board_history(board)


    def add_board_history(self, board):
        self.board_history.append(copy.deepcopy(board))

    # check if col is full or not
    def is_valid(self, board, col):
        return board[N_ROWS-1][col] == EMPTY

    # get first empty row in col
    def get_next_open_row(self, board, col):
        for r in range(N_ROWS):
            if board[r][col] == EMPTY: #if == 0, row empty so piece will drop in that row
                return r

    # check if putting the piece in the board, the player win
    def winning_move(self, board, piece):
        for c in range(N_COLS - 3): #check -
            for r in range(N_ROWS):
                if board[r][c] == piece and \
                        board[r][c+1] == piece and \
                        board[r][c+2] == piece and \
                        board[r][c+3] == piece:
                    return True

        for c in range(N_COLS):  # check |
            for r in range(N_ROWS - 3):
                if board[r][c] == piece and \
                        board[r + 1][c] == piece and \
                        board[r + 2][c] == piece and \
                        board[r + 3][c] == piece:
                    return True

        for c in range(N_COLS - 3): #check /
            for r in range(N_ROWS - 3):
                if board[r][c] == piece and \
                        board[r + 1][c + 1] == piece and \
                        board[r + 2][c + 2] == piece and \
                        board[r + 3][c + 3] == piece:
                    return True

        for c in range(N_COLS - 3): #check \
            for r in range(N_ROWS):
                if board[r][c] == piece and \
                        board[r - 1][c + 1] == piece and \
                        board[r - 2][c + 2] == piece and \
                        board[r - 3][c + 3] == piece:
                    return True

    # list of position in which the piece could drop (columns not empty)
    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(N_COLS):
            if self.is_valid(board, col):
                valid_locations.append(col)
        return valid_locations
