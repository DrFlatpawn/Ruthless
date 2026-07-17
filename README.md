# Ruthless ♟️

Ruthless is my attempt at building a chess engine from scratch in Python that speaks the UCI protocol. The goal isn't to compete with Stockfish (yet 😄), but to learn how modern chess engines work while making something that's actually fun to improve.

This project started as a personal challenge to understand search algorithms, evaluation functions, move ordering, and engine optimization.

## Features

- UCI compatible
- Alpha-Beta Negamax search
- Iterative Deepening
- Quiescence Search
- Transposition Table (Zobrist hashing)
- Killer Move Heuristic
- History Heuristic
- Late Move Reductions (LMR)
- Null Move Pruning
- Aspiration Windows
- PeSTO Piece-Square Tables
- Tapered Evaluation (Middlegame / Endgame)
- Basic Pawn Structure Evaluation
- Time Management for blitz and rapid

## Current Strength

Ruthless is still a work in progress.

It can already play complete games through any UCI-compatible GUI and on Lichess bots, but there is still a lot to improve in both evaluation and search quality.

Current goals include:

- Better king safety
- Better passed pawn evaluation
- Smarter move ordering
- Improved endgame play
- Search optimizations
- Stronger tactical vision

## Installation

Clone the repository

```bash
git clone https://github.com/DrFlatpawn/Ruthless.git
cd Ruthless
```

Install dependencies

```bash
pip install python-chess
```

Run the engine

```bash
python Ruthless.py
```

## Using with a GUI

Ruthless works with any UCI-compatible chess GUI, including:

- Arena
- Cute Chess
- Banksia GUI
- Lucas Chess
- Lichess Bot

Simply add `Ruthless.py` as a UCI engine (or compile it if you later package it as an executable).

## Project Structure

```
Ruthless.py
README.md
LICENSE
```

## Why Python?

Most strong chess engines are written in C++ for speed.

I chose Python because I wanted to focus on learning engine design first rather than low-level optimization. Once the search and evaluation become mature enough, I may rewrite the engine in C++.

## Roadmap

- [x] UCI protocol
- [x] Alpha-Beta Search
- [x] Quiescence Search
- [x] Transposition Table
- [x] Iterative Deepening
- [x] Killer Moves
- [x] History Heuristic
- [x] Aspiration Windows
- [ ] Opening Book
- [ ] Endgame Tablebases
- [ ] NNUE Evaluation
- [ ] MultiPV
- [ ] Multi-threading
- [ ] Syzygy Support
- [ ] SMP Search

## Contributing

This is mainly a personal learning project, but suggestions, ideas, and pull requests are always welcome.

## License

MIT License

---

Built because I wanted to understand how chess engines actually think.

## How to play with Ruthless?

You can play with Ruthless by sending him a challenge directly on lichess --> https://lichess.org/@/RuthlessBot
