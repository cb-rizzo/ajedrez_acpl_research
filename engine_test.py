import chess
import chess.engine
import chess.pgn

# Define file paths
pgn_filename = "sample.pgn"
stockfish_path = "./stockfish.exe"  

# Open Stockfish engine process
engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

# Limit engine analysis time per move (0.05 seconds per position for quick testing)
analysis_limit = chess.engine.Limit(time=0.05)

white_eval_losses = []
black_eval_losses = []

# Open and parse PGN file
with open(pgn_filename, encoding="utf-8") as pgn_file:
    game = chess.pgn.read_game(pgn_file)
    board = game.board()

    print(f"Analyzing game: {game.headers.get('White')} vs {game.headers.get('Black')}\n")

    for move in game.mainline_moves():
        # Evaluate position BEFORE making the move to know the optimal evaluation
        info_before = engine.analyse(board, analysis_limit)
        eval_before = info_before["score"].white()

        # Apply move to board
        is_white_turn = board.turn == chess.WHITE
        board.push(move)

        # Evaluate position AFTER the move
        info_after = engine.analyse(board, analysis_limit)
        eval_after = info_after["score"].white()

        # Calculate evaluation loss (CPL) for the player who moved
        if is_white_turn:
            # Score perspective is White
            score_before = eval_before.score(mate_score=10000)
            score_after = eval_after.score(mate_score=10000)
            loss = max(0, score_before - score_after)
            white_eval_losses.append(loss)
        else:
            # Score perspective is Black (invert values)
            score_before = -eval_before.score(mate_score=10000)
            score_after = -eval_after.score(mate_score=10000)
            loss = max(0, score_before - score_after)
            black_eval_losses.append(loss)

# Close Stockfish engine process safely
engine.quit()

# Calculate Average Centipawn Loss (ACPL)
acpl_white = sum(white_eval_losses) / len(white_eval_losses) if white_eval_losses else 0
acpl_black = sum(black_eval_losses) / len(black_eval_losses) if black_eval_losses else 0

print("-" * 50)
print(f"White ACPL: {acpl_white:.2f} centipawns")
print(f"Black ACPL: {acpl_black:.2f} centipawns")
print("-" * 50)