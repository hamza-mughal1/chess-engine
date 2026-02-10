# Python Chess Engine

A strong chess engine built from scratch in Python, featuring a custom evaluation function and optimizations like Alpha-Beta Pruning, Transposition Tables, and Quiescence Search.

![Chess Engine Preview](https://imgur.com/gallery/chessboard-0N5bwjQ#/t/chessboard)

## Features

*   **Minimax Algorithm** with **Alpha-Beta Pruning**
*   **Iterative Deepening** for efficient time management
*   **Transposition Table** with **Zobrist Hashing** (caching)
*   **Move Ordering** (MVV-LVA logic) for faster search
*   **Quiescence Search** to avoid the horizon effect
*   **Piece-Square Tables** for positional evaluation
*   **Interactive UI** built with **Pygame**

## Installation

You can run this project using `pip` or `uv`.

### Prerequisites
*   Python 3.8+

### Setup

1.  Clone the repository:
    ```bash
    git clone https://github.com/hamza-mughal1/chess-engine.git
    cd chess-engine
    ```

2.  Install dependencies:
    ```bash
    # Using uv (Recommended)
    uv sync

    # OR using pip
    pip install -r requirements.txt
    ```

## How to Play

Run the main script to start the game:

```bash
# Using uv
uv run main.py

# OR using python directly
python main.py
```

1.  The game will ask you to choose your color: `(w)hite` or `(b)lack`.
2.  Click a piece to select it.
3.  Click a valid target square (highlighted) to move.
4.  Watch the AI think and respond!

## Engine Stats

The engine prints real-time statistics in the console, including:
*   **Nodes Visited**: Total positions evaluated.
*   **Time Taken**: Duration of the search.
*   **NPS**: Nodes Per Second (search speed).
*   **Move History**: Standard Algebraic Notation (SAN).

## License

MIT License
