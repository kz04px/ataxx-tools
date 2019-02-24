import ataxx
import ataxx.pgn
from statistics import mean
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-pgn", required=True, type=str, help="Path to the game .pgn")
    args = parser.parse_args()

    # Check the input file
    if not os.path.isfile(args.pgn):
        print(F"FileNotFoundError: [Errno 2] No such file or directory: '{args.pgn}'")
        return

    num_games = 0
    game_lengths = []
    num_captures = [0]*20

    # Statistic -- Game results
    black_wins = 0
    white_wins = 0
    draws = 0

    # Statistic -- Move types
    num_null = 0
    num_single = 0
    num_double = 0

    # Statistic -- Result types
    num_50move = 0
    num_maxmoves = 0
    num_checkmate = 0
    num_stonecount = 0

    for game in ataxx.pgn.GameIterator(args.pgn):
        if game.headers["Result"] not in ["1-0", "0-1", "1/2-1/2"]:
            continue

        num_games += 1

        if num_games % 10 == 0:
            print(F"Processing game {num_games:04d}... ", end="")

        board = ataxx.Board(game.headers["FEN"])

        for idx, node in enumerate(game.main_line(), 1):
            move = node.move

            # Statistic -- Move types
            if move == ataxx.Move.null():
                num_null += 1
            elif move.is_single():
                num_single += 1
            else:
                num_double += 1

            # Get piece counts
            before_black, before_white, _, _ = board.count()

            board.makemove(move)

            # Get piece counts
            after_black, after_white, _, num_empty = board.count()

            black_change = after_black - before_black
            white_change = after_white - before_white

            if board.turn == ataxx.BLACK:
                gain = white_change
            else:
                gain = black_change

            assert gain >= 0
            assert gain <= 8

            # Statistic -- Num captures
            num_captures[gain] += 1

        # Statistic -- Game results
        if game.headers["Result"] == "1-0":
            black_wins += 1
        elif game.headers["Result"] == "0-1":
            white_wins += 1
        elif game.headers["Result"] == "1/2-1/2":
            draws += 1
        else:
            assert False

        # Statistics -- Result types
        if board.fifty_move_draw():
            num_50move += 1
        elif board.max_length_draw():
            num_maxmoves += 1
        elif after_black == 0 or after_white == 0:
            num_checkmate += 1
        else:
            num_stonecount += 1

        game_lengths.append(idx)

        if num_games % 10 == 0:
            print("done")

    assert num_games == len(game_lengths)
    assert num_games == black_wins + white_wins + draws
    assert num_games == num_50move + num_maxmoves + num_checkmate + num_stonecount

    print(F"Games analysed: {num_games}")
    print("")

    print("--- Game length ---")
    print(F"Shortest game: {min(game_lengths)}")
    print(F"Longest game:  {max(game_lengths)}")
    print(F"Mean:          {mean(game_lengths)}")
    print("")

    print("--- Game Results ---")
    print(F"1-0:  {black_wins}")
    print(F"0-1:  {white_wins}")
    print(F"draw: {draws}")
    print("")

    print("--- Result types ---")
    print(F"50move:    {num_50move}")
    print(F"length:    {num_maxmoves}")
    print(F"checkmate: {num_checkmate}")
    print(F"stones:    {num_stonecount}")
    print("")

    print("--- Move types ---")
    print(F"Null moves:   {num_null}")
    print(F"Single moves: {num_single}")
    print(F"Double moves: {num_double}")
    print("")

    print("--- Stones captured ---")
    for i in range(9):
        print(F"{i}: {num_captures[i]}")
    print("")

    print("--- Other ---")
    print(F"Stones captured per game: {sum(num_captures)/num_games}")
    print("")

if __name__ == "__main__":
    main()
