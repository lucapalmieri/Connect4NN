import random
import copy
import csv
import os

from game import Game
from minmax import Minmax
from neuralNetwor import NeuralNetwork

TURN_PLAYER_1 = 0
PLAYER_1_PIECE = 1
PLAYER_2_PIECE = 2

N_ROWS = 6
N_COLS = 7

HUMAN = 0
AI_RANDOM = 1
AI_MINMAX = 2
AI_NN = 3
AI_NN_NON_DET = 4

# to increase the "intelligence" of Minmax algorithm, increase the depth. Represent how much the algorithm look ahead in the three
DEPTH_MINMAX = 3


class Controller:

    def __init__(self):
        self.game = Game()
        self.minmax = Minmax()
        self.neuralNetwork = NeuralNetwork(42, 3, 512, 200)


    def human_turn(self, board, n_player):
        col = input("\nPlayer n. {}: insert number in range 0-6: ".format(n_player))

        while not col.isdigit():
            print("Type insert is not a number...")
            col = input("\nPlayer n. {}: insert number in range 0-6: ".format(n_player))

        col = int(col)

        while not 0 <= col <= N_COLS - 1:
            print("Column selected is not in range (0, 6).")
            col = input("\nPlayer n. {}: insert number in range 0-6: ".format(n_player))
            while not col.isdigit():
                print("Type insert is not a number...")
                col = input("\nPlayer n. {}: insert number in range 0-6: ".format(n_player))
            col = int(col)

        if self.game.is_valid(board, col):
            self.game.drop(board, col, n_player)
        else:
            while not self.game.is_valid(board, col):
                col = input("\nERROR! Column {} is full.\nPlayer n. {}: insert number in range 0-6: ".format(col, n_player))
                while not col.isdigit():
                    print("Type insert is not a number...")
                    col = input("\nPlayer n. {}: insert number in range 0-6: ".format(n_player))

                col = int(col)

                while not 0 <= col <= N_COLS - 1:
                    print("Column selected is not in range 0-6.")
                    col = input("\nPlayer n. {}: insert number in range 0-6: ".format(n_player))
                    while not col.isdigit():
                        print("Type insert is not a number...")
                        col = input("\nPlayer n. {}: insert number in range 0-6: ".format(n_player))
                    col = int(col)


    def randomAI_turn(self, board, n_player, showPrint):
        if showPrint:
            print("\nPlayer n. {}: Random AI thinking....".format(n_player))
        col = random.choice(self.game.get_valid_locations(board))
        self.game.drop(board, col, n_player)
        if showPrint:
            print("Column chosen: {}".format(col))


    def minmaxAI_turn(self, board, n_player, showPrint):
        if showPrint:
            print("\nPlayer n. {}: Minmax AI thinking....".format(n_player))
        col, minimax_score = self.minmax.minmax(board, DEPTH_MINMAX, True)

        if self.game.is_valid(board, col):
            self.game.drop(board, col, n_player)
        else:
            col = random.choice(self.game.get_valid_locations(board))
            self.game.drop(board, col, n_player)

        if showPrint:
            print("Column chosen: {}".format(col))


    def neuralNetworkAI_turn(self, board, n_player, showPrint):
        if showPrint:
            print("\nPlayer n. {}: Neural Network AI thinking....".format(n_player))
        max_value = 0
        valid_locations = self.game.get_valid_locations(board)
        best_move = valid_locations[0]
        for valid_location in valid_locations:
            b_copy = copy.deepcopy(board)
            self.game.drop(b_copy, valid_location, n_player)
            value = self.neuralNetwork.predict(b_copy)[0][n_player]
            if value > max_value:
                max_value = value
                best_move = valid_location
            if showPrint:
                print("N. {} value={}".format(valid_location, value))
        if showPrint:
            print("Column chosen: {}".format(best_move))
        self.game.drop(board, best_move, n_player)


    def neuralNetworkAI_nonDeterministic_turn(self, board, n_player, showPrint):
        if showPrint:
            print("\nPlayer n. {}: Neural Network AI thinking....".format(n_player))
        valid_locations = self.game.get_valid_locations(board)
        choice = []
        for valid_location in valid_locations:
            b_copy = copy.deepcopy(board)
            self.game.drop(b_copy, valid_location, n_player)
            value = round((self.neuralNetwork.predict(b_copy)[0][n_player])*100)
            for i in range(value):
                choice.append((valid_location, value))

        col = random.choice(choice)[0]
        self.game.drop(board, col, n_player)
        if showPrint:
            print("Column chosen: {}".format(col))

    def choose_players(self):
        print("\nChoose player 1:"
              "\n0 - Human"
              "\n1 - AI Random"
              "\n2 - AI MinMax"
              "\n3 - AI Neural Net"
              "\n4 - AI Neural Net (non deterministic)")

        player1 = input("\nPlayer1: ")

        while not player1.isdigit() or not 0 <= int(player1) <= 4:
            player1 = input("\nPlease insert a number in range 0-4 for Player 1:")

        player1 = int(player1)

        print("\nChoose player 2:"
              "\n0 - Human"
              "\n1 - AI Random"
              "\n2 - AI MinMax"
              "\n3 - AI Neural Net"
              "\n4 - AI Neural Net (non deterministic)")

        player2 = input("\nPlayer2: ")

        while not player2.isdigit() or not 0 <= int(player2) <= 4:
            player2 = input("\nPlease insert a number in range 0-4 for Player 2:")

        player2 = int(player2)

        return player1, player2


    def initialize_games(self):
        datasetName = ""
        player1, player2 = self.choose_players()

        if player1 in [AI_NN, AI_NN_NON_DET] or player2 in [AI_NN, AI_NN_NON_DET]:
            selection_train_load = input("\nDo you want to train a new model or load an old one? (t/l): ")

            while selection_train_load not in ['t', 'l'] or not selection_train_load.isalpha():
                selection_train_load = input("\nPlease insert t to train a new model, l to load a previous one: ")

            selection_train_load = selection_train_load[0]

            if selection_train_load == 't':
                selection_dataset_new_old = input("\nDo you want to use an existing dataset? (y/n): ")

                while selection_dataset_new_old not in ['y', 'n'] or not selection_dataset_new_old.isalpha():
                    selection_dataset_new_old = input("\nPlease insert y or n : ")

                selection_dataset_new_old = selection_dataset_new_old[0]

                if selection_dataset_new_old == 'n':  # Do you want to use an existing dataset? (y/n)
                    datasetName = input("\nInsert the name of the new dataset (without .csv): ")
                    numGamesDataset = input("\nHow many games do you want to simulate for the dataset {}.csv? ".format(datasetName))

                    while not numGamesDataset.isdigit() or not int(numGamesDataset) > 0:
                        print("\nPlease insert a positive integer..")
                        numGamesDataset = input("\nHow many games do you want to simulate for the dataset {}.csv? ".format(datasetName))

                    numGamesDataset = int(numGamesDataset)

                    datasetPlayer1, datasetPlayer2 = self.choose_players()
                    self.create_csv_file(datasetName, numGamesDataset, datasetPlayer1, datasetPlayer2)
                    datasetName = datasetName + ".csv"

                elif selection_dataset_new_old == 'y': # Do you want to use an existing dataset? (y/n)
                    for name in sorted(os.listdir("dataset")):
                        if not name.startswith("."):
                            print(name)
                    datasetName = input("\nSelect one of the names above: ")

                    while datasetName not in os.listdir("dataset"):
                        datasetName = input("\nDataset selected doesn't exists. \nPlease select one od the names above: ")

                selection_dataset_dupl = input("\nDo you want to drop duplicate board state? (y/n): ")

                while selection_dataset_dupl not in ['y', 'n'] or not selection_dataset_dupl.isalpha():
                    selection_dataset_dupl = input("\nPlease insert y or n : ")

                selection_dataset_dupl = selection_dataset_dupl[0]

                if selection_dataset_dupl == 'y':
                    self.neuralNetwork.train("dataset/" + datasetName, True)
                elif selection_dataset_dupl == 'n':
                    self.neuralNetwork.train("dataset/" + datasetName, False)

            elif selection_train_load == 'l':
                for name in sorted(os.listdir("modelSaved")):
                    print(name)

                modelName = input("\nSelect one of the names above: ")
                while modelName not in os.listdir("modelSaved"):
                    modelName = input("\nModel selected doesn't exists. \nPlease select one od the names above: ")

                self.neuralNetwork.load("modelSaved/" + modelName)

        n_games = input("\nHow many games do you want to play? ")

        while not n_games.isdigit() or not int(n_games) > 0:
            print("\nPlease insert a positive integer..")
            n_games = input("How many games do you want to play? ")

        n_games = int(n_games)

        return player1, player2, n_games


    def create_csv_file(self, name, numberGames, player1, player2):
        with open("dataset/" + name + ".csv", 'w') as file:
            writer = csv.writer(file)
            print("------------------------------Creating {}.csv------------------------------".format(name))
            for i in range(numberGames):
                if (i + 1) % 1000 == 0:
                    print("simulated {}/{} games, {}%".format(i + 1, numberGames, round(((i + 1) / numberGames) * 100, 2)))
                result, moves = self.play_single_game(player1, player2, False)
                for board in self.game.get_board_history():
                    writer.writerow((result, board))


    def play_single_game(self, player1, player2, showPrint):
        game_over = False
        turn = TURN_PLAYER_1
        n_moves = 0
        n_max_moves = N_ROWS * N_COLS
        result = 0
        board = self.game.create_board()

        if showPrint:
            self.game.print_board(board)

        while not game_over:
            if n_moves < n_max_moves:
                if turn == TURN_PLAYER_1:
                    if player1 == HUMAN:
                        self.human_turn(board, PLAYER_1_PIECE)
                        n_moves += 1
                    elif player1 == AI_RANDOM:
                        if showPrint:
                            self.randomAI_turn(board, PLAYER_1_PIECE, True)
                        else:
                            self.randomAI_turn(board, PLAYER_1_PIECE, False)
                        n_moves += 1
                    elif player1 == AI_MINMAX:
                        if showPrint:
                            self.minmaxAI_turn(board, PLAYER_1_PIECE, True)
                        else:
                            self.minmaxAI_turn(board, PLAYER_1_PIECE, False)
                        n_moves += 1
                    elif player1 == AI_NN:
                        if showPrint:
                            self.neuralNetworkAI_turn(board, PLAYER_1_PIECE, True)
                        else:
                            self.neuralNetworkAI_turn(board, PLAYER_1_PIECE, False)
                        n_moves += 1
                    else:
                        if showPrint:
                            self.neuralNetworkAI_nonDeterministic_turn(board, PLAYER_1_PIECE, True)
                        else:
                            self.neuralNetworkAI_nonDeterministic_turn(board, PLAYER_1_PIECE, False)
                        n_moves += 1

                    if self.game.winning_move(board, PLAYER_1_PIECE):
                        result = 1
                        game_over = True
                else:
                    if player2 == HUMAN:
                        self.human_turn(board, PLAYER_2_PIECE)
                        n_moves += 1
                    elif player2 == AI_RANDOM:
                        if showPrint:
                            self.randomAI_turn(board, PLAYER_2_PIECE, True)
                        else:
                            self.randomAI_turn(board, PLAYER_2_PIECE, False)
                        n_moves += 1
                    elif player2 == AI_MINMAX:
                        if showPrint:
                            self.minmaxAI_turn(board, PLAYER_2_PIECE, True)
                        else:
                            self.minmaxAI_turn(board, PLAYER_2_PIECE, False)
                        n_moves += 1
                    elif player2 == AI_NN:
                        if showPrint:
                            self.neuralNetworkAI_turn(board, PLAYER_2_PIECE, True)
                        else:
                            self.neuralNetworkAI_turn(board, PLAYER_2_PIECE, False)
                        n_moves += 1
                    else:
                        if showPrint:
                            self.neuralNetworkAI_nonDeterministic_turn(board, PLAYER_2_PIECE, True)
                        else:
                            self.neuralNetworkAI_nonDeterministic_turn(board, PLAYER_2_PIECE, False)
                        n_moves += 1

            else:
                result = 0
                game_over = True

            if showPrint:
                self.game.print_board(board)

            turn += 1
            turn = turn % 2

        if showPrint:
            if result == 0:
                print("\nDraw")
            elif result == 1:
                print("\nPlayer 1 Win")
            else: #result == 2
                print("\nPlayer 2 Win")

        return result, n_moves


    def play_multiple_games(self, player1, player2, n_games, showPrint):
        win_player_1 = 0
        win_player_2 = 0
        draws = 0
        n_moves = 0
        moves_list = []

        for i in range(n_games):
            if showPrint:
                print("--------------------Game n. {}--------------------".format(i + 1))

            game_result, moves = self.play_single_game(player1, player2, showPrint)
            moves_list.append(moves)
            n_moves += moves

            if game_result == PLAYER_1_PIECE:
                win_player_1 += 1
            elif game_result == PLAYER_2_PIECE:
                win_player_2 += 1
            else:  # self.play_game() == 0
                draws += 1

        perc_win_1 = round((win_player_1 / n_games) * 100, 2)
        perc_win_2 = round((win_player_2 / n_games) * 100, 2)
        perc_draw = round((draws / n_games) * 100, 2)
        avg_moves = round((n_moves/n_games), 2)

        if showPrint:
            print("\nFirst player win {}/{}: {}%".format(win_player_1, n_games, perc_win_1))
            print("Second player win {}/{}: {}%".format(win_player_2, n_games, perc_win_2))
            print("Total draw {}/{}: {}%".format(draws, n_games, perc_draw))
            print("Average of pieces dropped: {}".format(avg_moves))