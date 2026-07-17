# Ruthless ♟️

Ruthless is my attempt at building a chess engine from scratch in Python that speaks the UCI protocol. The goal isn't to compete with Stockfish (yet 😄), but to learn how modern chess engines work while making something that's actually fun to improve.

This project started as a personal challenge to understand search algorithms, evaluation functions, move ordering, and engine optimization.

## Features
- UCI compatible
- Alpha-Beta Negamax search
- Iterative Deepening
- Quiescence Search (with check evasions + delta pruning)
- Transposition Table (Zobrist hashing)
- Killer Move Heuristic
- History Heuristic
- Late Move Reductions (LMR)
- Principal Variation Search (PVS)
- Null Move Pruning
- Reverse Futility / Futility Pruning
- Check Extensions
- Aspiration Windows
- PeSTO Piece-Square Tables
- Tapered Evaluation (Middlegame / Endgame)
- Pawn Structure Evaluation (doubled, isolated, passed pawns)
- Mobility Evaluation
- King Safety Evaluation
- Time Management for blitz, rapid, and bullet

## Current Strength
Ruthless is still a work in progress.
It can already play complete games through any UCI-compatible GUI and on Lichess bots, but there is still a lot to improve in both evaluation and search quality.

Current goals include:
- Smarter move ordering
- Improved endgame play
- Further search optimizations
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
- [x] Late Move Reductions
- [x] Principal Variation Search
- [x] Check Extensions
- [x] Futility Pruning
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
