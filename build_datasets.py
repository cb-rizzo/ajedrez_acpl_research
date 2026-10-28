import io
import requests
import zstandard as zstd
import chess.pgn
import pandas as pd
import chess.engine
from dataset_processor import parse_and_evaluate_game


def fetch_and_filter_cohort(
    url: str,
    target_year: str,
    target_min_elo: int = 1100,
    target_max_elo: int = 1300,
    max_filtered_games: int = 100,
    engine_path: str = "./stockfish.exe",
) -> pd.DataFrame:
    """To download open data stream, filter by ELO and time control, and evaluate cohort games."""
    print(f"\n[+] Fetching cohort for year {target_year} (Target: {max_filtered_games} games)...")

    headers = {"User-Agent": "ACPL-Research-Project/1.0"}
    # Download ~100 MB chunk to get enough matching filtered games
    range_headers = {"Range": "bytes=0-104857600"}
    range_headers.update(headers)

    try:
        response = requests.get(url, headers=range_headers, timeout=60)
        if response.status_code not in (200, 206):
            print(f"[-] Failed to fetch data for year {target_year}. Status: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"[-] Network error fetching dataset: {e}")
        return pd.DataFrame()

    dctx = zstd.ZstdDecompressor()
    stream_reader = dctx.stream_reader(io.BytesIO(response.content))
    text_stream = io.TextIOWrapper(stream_reader, encoding="utf-8", errors="ignore")

    engine = chess.engine.SimpleEngine.popen_uci(engine_path)
    all_evaluated_data = []
    games_processed = 0

    while games_processed < max_filtered_games:
        try:
            game = chess.pgn.read_game(text_stream)
        except Exception:
            break

        if game is None:
            break

        headers_dict = game.headers
        try:
            white_elo = int(headers_dict.get("WhiteElo", 0))
            black_elo = int(headers_dict.get("BlackElo", 0))
        except ValueError:
            continue

        time_control = headers_dict.get("TimeControl", "")

        # Filter by ELO range for both players
        if (target_min_elo <= white_elo <= target_max_elo) and (
            target_min_elo <= black_elo <= target_max_elo
        ):
            eval_results = parse_and_evaluate_game(game, engine)
            for row in eval_results:
                row["cohort_year"] = target_year
                row["time_control"] = time_control
                all_evaluated_data.append(row)

            games_processed += 1
            if games_processed % 10 == 0 or games_processed == max_filtered_games:
                print(f"    -> Progress [{target_year}]: {games_processed}/{max_filtered_games} games evaluated")

    engine.quit()
    return pd.DataFrame(all_evaluated_data)


if __name__ == "__main__":
    url_2019 = "https://database.lichess.org/standard/lichess_db_standard_rated_2019-01.pgn.zst"
    url_recent = "https://database.lichess.org/standard/lichess_db_standard_rated_2024-01.pgn.zst"

    # Cohort 2019: Target baseline 1100-1300 ELO (100 games)
    df_2019 = fetch_and_filter_cohort(
        url_2019,
        target_year="2019",
        target_min_elo=1100,
        target_max_elo=1300,
        max_filtered_games=100,
    )

    # Cohort 2026/Recent: Extended range 800-1300 ELO for calibration (100 games)
    df_recent = fetch_and_filter_cohort(
        url_recent,
        target_year="2026",
        target_min_elo=800,
        target_max_elo=1300,
        max_filtered_games=100,
    )

    # Merge datasets and save to CSV
    df_full = pd.concat([df_2019, df_recent], ignore_index=True)
    if not df_full.empty:
        df_full.to_csv("chess_acpl_cohorts.csv", index=False)
        print(f"\n[✓] Successfully built final dataset with {len(df_full)} player-records in 'chess_acpl_cohorts.csv'")