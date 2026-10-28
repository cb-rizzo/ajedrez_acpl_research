import math
import chess
import chess.engine
import chess.pgn
import pandas as pd


def count_pieces_excluding_kings(board: chess.Board) -> int:
    """To count total pieces remaining on the board excluding both kings."""
    total_pieces = 0
    for piece_type in [
        chess.PAWN,
        chess.KNIGHT,
        chess.BISHOP,
        chess.ROOK,
        chess.QUEEN,
    ]:
        total_pieces += len(board.pieces(piece_type, chess.WHITE))
        total_pieces += len(board.pieces(piece_type, chess.BLACK))
    return total_pieces


def parse_and_evaluate_game(
    game: chess.pgn.Game, engine: chess.engine.SimpleEngine, time_limit: float = 0.05
) -> list:
    """To parse a PGN game, evaluate moves with Stockfish, and extract phase-segmented metrics including blunder rates."""
    headers = game.headers
    board = game.board()

    # 1. Initialize blunder counters
    metrics = {
        chess.WHITE: {
            "cpl_opening": [],
            "cpl_middlegame": [],
            "cpl_endgame": [],
            "cpl_all": [],
            "blunder_count": 0,
        },
        chess.BLACK: {
            "cpl_opening": [],
            "cpl_middlegame": [],
            "cpl_endgame": [],
            "cpl_all": [],
            "blunder_count": 0,
        },
    }

    move_index = 1

    for move in game.mainline_moves():
        current_color = board.turn

        # To evaluate optimal score before making move
        info_before = engine.analyse(board, chess.engine.Limit(time=time_limit))
        score_before_obj = info_before["score"].pov(current_color)
        score_before = score_before_obj.score(mate_score=10000)

        # To push move and evaluate resulting score
        board.push(move)
        info_after = engine.analyse(board, chess.engine.Limit(time=time_limit))
        score_after_obj = info_after["score"].pov(current_color)
        score_after = score_after_obj.score(mate_score=10000)

        # To calculate raw CPL
        raw_cpl = max(0, score_before - score_after)
        
        # 2. Evaluates blunder threshold (raw_cpl >= 300 cp / decisive piece or advantage loss)
        if raw_cpl >= 300:
            metrics[current_color]["blunder_count"] += 1

        # Capped CPL for global averages
        capped_cpl = min(raw_cpl, 300)

        # To determine game phase
        pieces_left = count_pieces_excluding_kings(board)
        if move_index <= 20:  # Moves 1-10 (20 ply)
            phase = "cpl_opening"
        elif pieces_left > 6:
            phase = "cpl_middlegame"
        else:
            phase = "cpl_endgame"

        metrics[current_color][phase].append(capped_cpl)
        metrics[current_color]["cpl_all"].append(capped_cpl)

        move_index += 1

    # 3. Constructs final record output including blunder_count and blunder_rate
    results = []
    for color in [chess.WHITE, chess.BLACK]:
        all_moves = metrics[color]["cpl_all"]
        total_moves = len(all_moves)
        blunders = metrics[color]["blunder_count"]
        
        # Blunder rate per 100 moves
        blunder_rate = (blunders / total_moves * 100) if total_moves > 0 else 0.0

        color_str = "White" if color == chess.WHITE else "Black"
        player_name = headers.get(color_str, "Unknown")
        player_elo = headers.get(f"{color_str}Elo", "0")

        results.append({
            "site": headers.get("Site", ""),
            "date": headers.get("UTCDate", ""),
            "player_color": color_str,
            "player_name": player_name,
            "player_elo": player_elo,
            "acpl_global": sum(all_moves) / total_moves if total_moves > 0 else None,
            "median_cpl": float(pd.Series(all_moves).median()) if total_moves > 0 else None,
            "std_cpl": float(pd.Series(all_moves).std()) if total_moves > 0 else None,
            "blunder_count": blunders,
            "blunder_rate": round(blunder_rate, 2),
            "acpl_opening": sum(metrics[color]["cpl_opening"]) / len(metrics[color]["cpl_opening"]) if metrics[color]["cpl_opening"] else None,
            "acpl_middlegame": sum(metrics[color]["cpl_middlegame"]) / len(metrics[color]["cpl_middlegame"]) if metrics[color]["cpl_middlegame"] else None,
            "acpl_endgame": sum(metrics[color]["cpl_endgame"]) / len(metrics[color]["cpl_endgame"]) if metrics[color]["cpl_endgame"] else None,
        })

    return results


# To execute test execution if run directly
if __name__ == "__main__":
    stockfish_path = "./stockfish.exe"
    pgn_filename = "lichess_sample.pgn"

    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    with open(pgn_filename, encoding="utf-8") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        analysis_data = parse_and_evaluate_game(game, engine)

    engine.quit()

    # To display output as Pandas DataFrame
    df = pd.DataFrame(analysis_data)
    print(df.to_string())