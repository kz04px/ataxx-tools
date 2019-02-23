import ataxx
import ataxx.pgn
import matplotlib.pyplot as plt
import argparse
import os

def graph(path, title, black, white, max_pieces):
    plt.figure()

    # Stone plots
    plt.plot(black, label="Black")
    plt.plot(white, label="White")

    # X axis
    plt.xlabel('ply')
    plt.xlim((0, round(len(black), -1)))

    # Marker for 50% of the board
    plt.axhline(y=max_pieces/2, color='r', linestyle='-')

    # Y axis
    plt.ylabel('stones')
    plt.ylim((0, 50))

    plt.title(title, fontsize=12)
    plt.legend(loc='upper center', bbox_to_anchor=(0.2, 0.95), fancybox=True, shadow=False)
    plt.savefig(path, dpi=150)
    plt.clf()

def main(path, directory):
    # Check the input file
    if not os.path.isfile(path):
        print(F"File \"{path}\" doesn't exist")
        return

    # Check the output directory
    if not os.path.isdir(directory):
        print(F"Directory \"{directory}\" doesn't exist")
        return

    for idx, game in enumerate(ataxx.pgn.GameIterator(path), 1):
        print(F"Processing game {idx:04d}... ", end="")

        board = ataxx.Board(game.headers["FEN"])

        # Number of pieces
        black = []
        white = []

        # Get piece counts
        num_black, num_white, _, num_empty = board.count()

        # Max pieces
        max_pieces = num_black + num_white + num_empty

        # Track piece count history
        black.append(num_black)
        white.append(num_white)

        for node in game.main_line():
            board.makemove(node.move)

            # Get piece counts
            num_black, num_white, _, _ = board.count()

            # Track piece count history
            black.append(num_black)
            white.append(num_white)

        if 'Black' in game.headers:
            black_player = game.headers['Black'][:40]
        else:
            black_player = "Unknown"

        if 'White' in game.headers:
            white_player = game.headers['White'][:40]
        else:
            white_player = "Unknown"

        # Try accommodate particularly long player names
        if len(black_player) + len(white_player) > 48:
            title = F"{black_player}\nvs\n{white_player}"
        else:
            title = F"{black_player} vs {white_player}"

        graph(F"{directory}/game_{idx:04d}.png", title, black, white, max_pieces)

        print("done")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create stone count graphs from ataxx games.')
    parser.add_argument('-pgn', type=str, required=True, help='path to the .pgn file to parse')
    parser.add_argument('-out', type=str, required=False, default="./", help='path to the output folder')
    args = parser.parse_args()

    main(args.pgn, args.out)
