import requests


def fetch_public_games(
    max_games: int = 5, output_filename: str = "lichess_sample.pgn"
) -> None:
    """To fetch recent public rated games directly from Lichess without needing specific usernames."""
    # Lichess endpoint for recent top/public games
    url = "https://lichess.org/api/tv/channels"

    print("To request recent public games from Lichess API...")

    try:
        # Request current active games on Lichess channels
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            channels_data = response.json()
            # Extract game IDs from active channels (Blitz, Rapid, Classical, etc.)
            game_ids = []
            for channel_name, channel_info in channels_data.items():
                if "gameId" in channel_info:
                    game_ids.append(channel_info["gameId"])

            # Limit to desired number of games
            selected_ids = game_ids[:max_games]

            if not selected_ids:
                print("No active game IDs retrieved.")
                return

            # Download PGNs for retrieved game IDs
            pgn_url = (
                f"https://lichess.org/api/games/export/_bulk"
            )
            pgn_response = requests.post(
                pgn_url,
                headers={"Accept": "application/x-chess-pgn"},
                data=",".join(selected_ids),
                timeout=10,
            )

            if pgn_response.status_code == 200:
                with open(output_filename, "w", encoding="utf-8") as f:
                    f.write(pgn_response.text)
                print(
                    f"Successfully downloaded and saved {len(selected_ids)} games to '{output_filename}'"
                )
            else:
                print(
                    f"Failed to export PGNs. HTTP Status Code: {pgn_response.status_code}"
                )

        else:
            print(
                f"Failed to fetch channel data. HTTP Status Code: {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during API request: {e}")


if __name__ == "__main__":
    fetch_public_games(max_games=5, output_filename="lichess_sample.pgn")