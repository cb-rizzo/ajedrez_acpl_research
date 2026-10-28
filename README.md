# Lichess Data Pipeline & Tactical Precision Analysis (2019 vs 2026)

A Data Science and Engineering project built in Python to process and analyze large-scale compressed Lichess game archives (`.pgn.zst`), evaluating move precision and error rates across historical cohorts using Stockfish 16.

---

## 📌 Project Overview

This project explores historical variations in player move accuracy (Centipawn Loss - CPL) on Lichess between 2019 and 2026. 

Using Stockfish UCI engine integration, the pipeline extracts move evaluations to compare baseline precision, error volatility, and blunder rates across rating brackets.

### Key Observations & Technical Highlights
* **ELO vs. Precision Observations:** In our sampled cohorts, modern ~1000 ELO players display median baseline precision (Median CPL ≈ 30) comparable to ~1200 ELO players from 2019, though overall rating dynamics involve broader ecosystem variables.
* **Error Volatility:** While overall move accuracy aligns closely between calibrated cohorts, modern lower-bracket samples show a slightly higher blunder frequency (CPL >= 300 CP) under time pressure (~13% vs ~10%).
* **Data Engineering Focus:** Efficient processing of compressed PGN streams without loading full datasets into memory.

---

## 🛠️ Data Pipeline & Architecture

The project emphasizes efficient stream processing and metric extraction from raw chess archives:

Lichess Compressed Data (.pgn.zst)
       │
       ▼ (Streaming / Chunking)
fetch_open_data.py / build_datasets.py
       │
       ▼ (UCI Protocol Engine Evaluation)
dataset_processor.py (Stockfish 16)
       │
       ▼ (Aggregated Metrics Export)
chess_acpl_cohorts.csv
       │
       ▼ (Statistical EDA & Visuals)
eda.ipynb Notebook

### ⚡ Engine Configuration & Execution Notes
Evaluation Depth / Limits: Stockfish evaluations run with a fixed limit per position (e.g., depth=12 or time_limit=0.1s), balancing analytical accuracy with evaluation speed.

Concurrency: Stream parsing and UCI engine evaluation are structured to allow scalable multi-threading across processing cores.

Metrics Processed:
Median CPL & Standard Deviation: Robust measurement of baseline precision and move-to-move volatility.

Blunder Rate (%): Percentage of moves resulting in severe tactical errors (>= 300 CP).

Phase-Segmented CPL: Accuracy segmented across Opening, Middlegame, and Endgame transitions.

💻 Repository Structure
.
├── fetch_open_data.py     # Streaming utility for compressed zstd Lichess datasets
├── dataset_processor.py   # Stockfish UCI evaluation engine & metric calculation
├── build_datasets.py      # Cohort extraction and multi-year dataset builder
├── eda.ipynb              # Exploratory Data Analysis & visual plots
├── chess_acpl_cohorts.csv # Evaluated output dataset
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation

🚀 Setup & Execution
Environment Setup:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Stockfish Binary:
Download Stockfish 16 and place the executable binary (stockfish.exe or stockfish) in the project root directory.

Run Pipeline & Analysis:
python build_datasets.py
jupyter notebook
