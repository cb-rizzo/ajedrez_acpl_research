import chess.pgn

pgn_filename = "sample.pgn"

# Open and parse PGN file
with open(pgn_filename, encoding="utf-8") as pgn_file:
    game = chess.pgn.read_game(pgn_file)

    # Extract header metadata
    headers = game.headers
    white_player = headers.get("White", "Unknown")
    black_player = headers.get("Black", "Unknown")
    white_elo = headers.get("WhiteElo", "N/A")
    black_elo = headers.get("BlackElo", "N/A")

    print(f"Game: {white_player} ({white_elo}) vs {black_player} ({black_elo})")
    print("-" * 50)

    # Traverse board positions and print FEN strings
    board = game.board()
    move_number = 1

    for move in game.mainline_moves():
        board.push(move)

        # Print only first 6 moves to verify format
        if move_number <= 6:
            print(f"Move {move_number}: {move.uci()}")
            print(f"FEN position: {board.fen()}")
            print("-" * 30)

        move_number += 1

    print(f"\nProcess completed. Total moves: {move_number - 1}")