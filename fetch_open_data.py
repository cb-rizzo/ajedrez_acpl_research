import io
import requests
import zstandard as zstd


def download_lichess_open_data_sample(
    output_filename: str = "lichess_sample.pgn", max_games: int = 10
) -> None:
    """To download a small chunk from Lichess Open Data and extract sample PGN games."""
    # Official Lichess Open Data monthly dump URL
    url = "https://database.lichess.org/standard/lichess_db_standard_rated_2023-01.pgn.zst"

    print("To download sample chunk from Lichess Open Data repository...")

    headers = {"User-Agent": "ACPL-Research-Project/1.0"}

    try:
        # Request only the first 500 KB of the compressed file to save bandwidth
        range_headers = {"Range": "bytes=0-524288"}
        range_headers.update(headers)

        response = requests.get(url, headers=range_headers, timeout=15)

        if response.status_code in (200, 206):
            # Decompress streaming data chunk
            dctx = zstd.ZstdDecompressor()
            stream_reader = dctx.stream_reader(io.BytesIO(response.content))
            text_stream = io.TextIOWrapper(stream_reader, encoding="utf-8", errors="ignore")

            games_text = ""
            games_count = 0

            for line in text_stream:
                games_text += line
                if line.startswith("[Event "):
                    games_count += 1
                if games_count > max_games:
                    break

            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(games_text)

            print(f"Successfully saved {max_games} sample games to '{output_filename}'")
        else:
            print(f"Failed to fetch data chunk. HTTP Status Code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred during dataset fetch: {e}")


if __name__ == "__main__":
    download_lichess_open_data_sample(output_filename="lichess_sample.pgn", max_games=10)