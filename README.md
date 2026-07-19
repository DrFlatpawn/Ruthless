# Ruthless ♟️

Ruthless is my attempt at building a chess engine from scratch in Python that speaks the UCI protocol. The goal isn't to compete with Stockfish (yet 😄), but to learn how modern chess engines work while making something that's actually fun to improve.

This project started as a personal challenge to understand search algorithms, evaluation functions, move ordering, and engine optimization.

## Features
- UCI compatible
- Alpha beta negamax search
- Iterative deepening
- Quiescence search (with check evasions + delta pruning + static exchange evaluation, see below, we don't talk about v2.2's first draft)
- Transposition table (Zobrist hashing)
- Killer move heuristic
- History heuristic
- Late move reductions (LMR)
- Late move pruning (LMP)
- Principal variation search (PVS)
- Null move pruning
- Reverse futility / futility pruning
- Check extensions
- Aspiration windows (now with progressive widening because rage-quitting straight to full width every fail was embarrassing)
- Static exchange evaluation (SEE) for quiescence move ordering/pruning
- PeSTO piece square tables (the endgame king table is no longer secretly the knight table, more on that below)
- Tapered evaluation (middlegame / endgame)
- Pawn structure evaluation (doubled, isolated, passed pawns)
- "Safe" mobility evaluation (doesn't get excited about a knight hanging out on a square defended by a pawn anymore)
- King safety evaluation (open files + pawn shield)
- Time management for blitz, rapid, and bullet

## Current strength
Ruthless is still a work in progress.
It can already play complete games through any UCI-compatible GUI and on lichess bots, but there is still a lot to improve in both evaluation and search quality.

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

## Why python when you know it's shitty?
Most strong chess engines are written in C++ for speed yeah... 
I chose python because I wanted to focus on learning engine design first rather than pure dummy optimization. Once the search and evaluation become mature enough, I may rewrite the engine in C++.


## Contributing
This is mainly a personal learning project, but suggestions, ideas, and pull requests are always welcome.

## License
MIT License

---

Built because I wanted to understand how chess engines actually think.

## How to play with Ruthless?
You can play with Ruthless by sending him a challenge directly on lichess --> https://lichess.org/@/RuthlessBot
