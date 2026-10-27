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
) -> dict:
    """To parse a PGN game, evaluate moves with Stockfish, and extract phase-segmented metrics."""
    headers = game.headers
    board = game.board()

    # Storage for move metrics per color
    metrics = {
        chess.WHITE: {
            "cpl_opening": [],
            "cpl_middlegame": [],
            "cpl_endgame": [],
            "cpl_all": [],
        },
        chess.BLACK: {
            "cpl_opening": [],
            "cpl_middlegame": [],
            "cpl_endgame": [],
            "cpl_all": [],
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

        # To calculate raw CPL and apply maximum cap (300 cp)
        raw_cpl = max(0, score_before - score_after)
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

    # To calculate summary statistics for White and Black
    results = []
    for color, color_name in [(chess.WHITE, "White"), (chess.BLACK, "Black")]:
        cpl_all = metrics[color]["cpl_all"]
        cpl_op = metrics[color]["cpl_opening"]
        cpl_mid = metrics[color]["cpl_middlegame"]
        cpl_end = metrics[color]["cpl_endgame"]

        if not cpl_all:
            continue

        mean_acpl = sum(cpl_all) / len(cpl_all)
        median_cpl = pd.Series(cpl_all).median()
        std_cpl = pd.Series(cpl_all).std() if len(cpl_all) > 1 else 0.0

        results.append(
            {
                "site": headers.get("Site", "N/A"),
                "date": headers.get("Date", "N/A"),
                "player_color": color_name,
                "player_name": headers.get(color_name, "Unknown"),
                "player_elo": int(headers.get(f"{color_name}Elo", 0)),
                "acpl_global": round(mean_acpl, 2),
                "median_cpl": round(median_cpl, 2),
                "std_cpl": round(std_cpl, 2),
                "acpl_opening": round(sum(cpl_op) / len(cpl_op), 2)
                if cpl_op
                else None,
                "acpl_middlegame": round(sum(cpl_mid) / len(cpl_mid), 2)
                if cpl_mid
                else None,
                "acpl_endgame": round(sum(cpl_end) / len(cpl_end), 2)
                if cpl_end
                else None,
            }
        )

    return results


# To execute test execution if run directly
if __name__ == "__main__":
    stockfish_path = "./stockfish.exe"
    pgn_filename = "sample.pgn"

    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    with open(pgn_filename, encoding="utf-8") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        analysis_data = parse_and_evaluate_game(game, engine)

    engine.quit()

    # To display output as Pandas DataFrame
    df = pd.DataFrame(analysis_data)
    print(df.to_string())