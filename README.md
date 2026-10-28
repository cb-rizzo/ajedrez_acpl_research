# Lichess Data Pipeline & Tactical Precision Analysis (2019 vs 2026)

A Data Science and Engineering project built in Python to process and analyze large-scale compressed Lichess game archives (`.pgn.zst`), evaluating move precision and error rates across historical cohorts using Stockfish 16.

---

## 📌 Project Overview

This project explores historical variations in player move accuracy (Centipawn Loss - CPL) on Lichess between 2019 and 2026. 

Using Stockfish UCI engine integration, the pipeline extracts move evaluations to compare baseline precision, error volatility, and blunder rates across rating brackets.

### Key Observations & Technical Highlights
* **ELO vs. Precision Observations:** In our sampled cohorts, modern ~1000 ELO players display median baseline precision ($\text{Median CPL} \approx 30$) comparable to ~1200 ELO players from 2019, though overall rating dynamics involve broader ecosystem variables.
* **Error Volatility:** While overall move accuracy aligns closely between calibrated cohorts, modern lower-bracket samples show a slightly higher blunder frequency ($\text{CPL} \ge 300$) under time pressure ($\sim 13\%$ vs $\sim 10\%$).
* **Data Engineering Focus:** Efficient processing of compressed PGN streams without loading full datasets into memory.

---

## 🛠️ Data Pipeline & Architecture

The project emphasizes efficient stream processing and metric extraction from raw chess archives:
[ Lichess Compressed Data (.pgn.zst) ]
│
▼ (Streaming / Chunking)
[ fetch_open_data.py / build_datasets.py ]
│
▼ (Stockfish UCI Engine Evaluation)
[ dataset_processor.py ]
│
▼
[ chess_acpl_cohorts.csv ]
│
▼
[ eda.ipynb ] (Statistical Exploration & Visuals)
### Metrics Processed:
* **Median CPL & Standard Deviation:** Robust measurement of baseline precision and move-to-move volatility.
* **Blunder Rate (%):** Percentage of moves resulting in severe tactical errors ($\ge 300\text{ CP}$).
* **Phase-Segmented CPL:** Accuracy segmented across Opening, Middlegame, and Endgame transitions.

---

## 💻 Repository Structure

```text
.
├── fetch_open_data.py    # Streaming utility for compressed zstd Lichess datasets
├── dataset_processor.py  # Stockfish UCI evaluation engine & metric calculation
├── build_datasets.py     # Cohort extraction and multi-year dataset builder
├── eda.ipynb             # Exploratory Data Analysis & visual plots
├── chess_acpl_cohorts.csv # Evaluated output dataset
└── README.md             # Documentation
```

## 🚀 Setup & Execution

1. **Environment Setup:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install chess zstandard requests pandas matplotlib seaborn jupyter
   Stockfish Binary:
   Download Stockfish 16 and place the binary in the root directory.

   Run Pipeline & Analysis:
   Bash
   python build_datasets.py
   jupyter notebook
