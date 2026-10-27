import chess.pgn

pgn_filename = "sample.pgn"

# 1. Abrir y parsear el archivo PGN
with open(pgn_filename, encoding="utf-8") as pgn_file:
    game = chess.pgn.read_game(pgn_file)

    # 2. Extraer metadatos del encabezado
    headers = game.headers
    white_player = headers.get("White", "Desconocido")
    black_player = headers.get("Black", "Desconocido")
    white_elo = headers.get("WhiteElo", "N/A")
    black_elo = headers.get("BlackElo", "N/A")

    print(f"Partida: {white_player} ({white_elo}) vs {black_player} ({black_elo})")
    print("-" * 50)

    # 3. Recorrer el tablero e imprimir posiciones FEN
    board = game.board()
    move_number = 1

    for move in game.mainline_moves():
        board.push(move)

        # Imprimimos solo las primeras 6 jugadas para ver el formato
        if move_number <= 6:
            print(f"Jugada {move_number}: {move.uci()}")
            print(f"Posición FEN: {board.fen()}")
            print("-" * 30)

        move_number += 1

    print(f"\nProceso completado. Total de jugadas: {move_number - 1}")