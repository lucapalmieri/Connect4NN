from controller import Controller
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":

    player1, player2, n_games = Controller().initialize_games()

    if n_games == 1:
        Controller().play_single_game(player1, player2, True)
    else:
        Controller().play_multiple_games(player1, player2, n_games, True)