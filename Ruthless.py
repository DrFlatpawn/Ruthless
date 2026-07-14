#!/usr/bin/env python3
import sys
import time
import chess
import chess.polyglot

# ==============================================================================
# "RUTHLESS" - PART 1/2: EVALUATION AND DATA ARCHITECTURE
# ==============================================================================

# Game Phase Weights (used to transition smoothly from Middlegame to Endgame)
PAWN_PHASE   = 0
KNIGHT_PHASE = 1
BISHOP_PHASE = 1
ROOK_PHASE   = 2
QUEEN_PHASE  = 4
MAX_PHASE    = 24  # (4*1 + 4*1 + 4*2 + 2*4)

# Middlegame (MG) and Endgame (EG) Piece Values
MG_VALUES = {
    chess.PAWN: 82,
    chess.KNIGHT: 337,
    chess.BISHOP: 365,
    chess.ROOK: 477,
    chess.QUEEN: 1025,
    chess.KING: 0
}

EG_VALUES = {
    chess.PAWN: 94,
    chess.KNIGHT: 281,
    chess.BISHOP: 297,
    chess.ROOK: 512,
    chess.QUEEN: 936,
    chess.KING: 0
}

# ------------------------------------------------------------------------------
# HIGHLY OPTIMIZED PeSTO PIECE-SQUARE TABLES (Mirrored for Black dynamically)
# Array mapped directly to python-chess internal square index (0 to 63 / A1 to H8)
# ------------------------------------------------------------------------------

PST_MG = {
    chess.PAWN: [
          0,   0,   0,   0,   0,   0,   0,   0,
        -35,  -1, -20, -23, -15,  24,  38, -22,
        -26,  -4,  -4, -10,   3,   3,  33, -12,
        -27,  -2,  -5,  12,  17,   6,  10, -17,
        -14,  13,   6,  21,  17,  12,   9, -16,
         -6,   7,  26,  31,  65,  56,  25, -20,
         98, 134,  61,  95,  68, 126,  34, -11,
          0,   0,   0,   0,   0,   0,   0,   0
    ],
    chess.KNIGHT: [
        -73, -41, -13, -15, -11, -18, -41, -76,
        -74, -23, -16, -19,   1, -12, -33, -22,
        -23, -15,   2,   6,  14,  -3,  -1, -11,
        -18,  15,  16,  25,  23,  18,   8, -13,
        -13,  16,  23,  40,  35,  18,  22,  -7,
        -31,   8,  40,  49,  76,  46,  11, -18,
        -73, -41,  10, -16,  62,  17, -17, -23,
       -167, -89, -34, -49,  61, -97, -15, -107
    ],
    chess.BISHOP: [
        -29,  -4, -14, -10,  -6,  -8,  -4, -36,
        -18,   3,  11,  -7,   2,   6,  21,  -6,
         -7,   3,  -3,  -5,  -3, -10,  -4, -11,
         -3,   9,  12,  10,  15,  10,   3,  -5,
         -2,   8,  17,  25,  16,  13,   7,  -1,
        -14,  18,  21,  38,  27,  13,   9, -14,
         -9,  19,  16,  -9,  -7,  24,   4, -17,
        -33,  -4, -14, -21, -13, -12, -39, -21
    ],
    chess.ROOK: [
         -6,   5,   9,   8,  17,  12,   3, -10,
        -14, -12, -10,  -7,   0, -12,  -5, -11,
        -10,  -7,  -3,  -4,  -3,  -8,  -2, -9,
         -9,   0,  -6,  -3,  -3,  -6,  -5,  -1,
         -1,   1,   4,  -6,   1,  -4,  -6,  -6,
          7,   7,   7,   5,   4,  -3,  -5,  -3,
         11,  13,  13,  14,  -3,   5,   1,  10,
         13,  10,  18,  15,  12,  12,   8,   5
    ],
    chess.QUEEN: [
        -19, -18, -11,  -5,  -7,  -7, -11, -20,
        -24, -13,  -7,  -1,  -1,  -5,  -5, -17,
        -20, -18, -13, -12, -10, -11, -16, -20,
        -16, -13,  -5,  -3,  -3,   0,  -2, -13,
         -1, -15,   2,  12,   8,  -2,   3,   0,
        -20,  10,  11,   4,  13,  18,  34,  -6,
        -17, -19,  -5,  -4, -14,  13,   0,   9,
         -9,  22,  22,  23,  27,  11,  10,  20
    ],
    chess.KING: [
         18,  30,  21,  10,  17,  27,  39,  22,
         14,  14,  14,  12,  11,  15,  22,  15,
         -5, -11, -10,  -7,  -8,  -4,   0,  -9,
        -17, -23, -21, -24, -21, -24, -13, -15,
        -21, -29, -29, -32, -31, -30, -24, -28,
        -27, -28, -27, -29, -30, -25, -17, -35,
        -28, -25, -24, -28, -30, -16, -17, -39,
        -24, -11,  -7, -14, -25, -18, -22, -29
    ]
}

PST_EG = {
    chess.PAWN: [
          0,   0,   0,   0,   0,   0,   0,   0,
         -8,  -7,  -7,  -8,  -8,  -7,  -6,  -8,
         -5,  -5,  -5,  -4,  -5,  -6,  -5,  -5,
         10,   8,   7,   7,   6,   4,   4,   9,
         38,  38,  34,  36,  34,  33,  34,  35,
         66,  65,  67,  68,  68,  66,  64,  65,
         94,  89,  94,  95,  93,  97,  96,  94,
          0,   0,   0,   0,   0,   0,   0,   0
    ],
    chess.KNIGHT: [
        -50, -38, -31, -27, -24, -30, -38, -50,
        -37, -25, -23, -15, -24, -21, -32, -37,
        -24, -13,  -6,   1,  -2,  -7, -14, -18,
         -7,  -3,   8,   9,  11,   4,  -1, -12,
         -3,   3,  12,  11,  12,   7,  -1,  -9,
        -13,  -5,   5,   1,   0,  -5, -12, -20,
        -25,  -8, -25,  -4,  -9, -14, -24, -29,
        -58, -38, -13, -28, -31, -27, -25, -99
    ],
    chess.BISHOP: [
        -14, -14, -11, -10, -10,  -7, -15, -14,
        -10,  -8,  -7,  -4,  -3,  -6,  -8, -14,
         -6,  -4,  -1,  -1,   1,   1,  -8, -10,
         -2,   0,   4,   5,   4,   4,  -4,  -4,
         -1,   4,   4,   4,   3,   1,  -3,  -6,
         -2,   4,   2,   4,   2,   3,  -4,  -8,
         -8,  -4,  -7,  -3,  -4,  -5, -10, -15,
        -14, -21, -11,  -8,  -7,  -9, -17, -24
    ],
    chess.ROOK: [
        -16, -16, -13, -11, -15, -10, -16, -20,
        -15, -17, -15, -15, -15, -16, -17, -17,
        -11, -13, -13, -11, -11, -12, -14, -14,
         -5,  -8,  -8,  -5,  -7,  -7,  -9,  -9,
          0,  -4,  -4,  -1,  -3,  -4,  -6,  -6,
          5,   1,   0,   2,   1,  -1,  -4,  -3,
          9,   5,   4,   7,   2,   3,  -2,  -1,
         11,   6,   5,   8,   7,   7,   3,   0
    ],
    chess.QUEEN: [
        -18, -13, -11,  -9,  -9, -11, -14, -18,
        -14,  -9,  -5,  -5,  -4,  -6,  -9, -14,
         -8,  -4,  -1,   0,   1,   0,  -4,  -9,
         -4,   0,   3,   4,   4,   2,   0,  -6,
         -4,   1,   3,   5,   4,   3,   1,  -6,
         -9,  -4,   0,   2,   1,  -1,  -4, -10,
        -14,  -4,  -5,  -1,  -3,  -7,  -6, -13,
        -18,  -9,  -9,  -5,  -5, -10, -11, -18
    ],
    chess.KING: [
        -58, -38, -13, -28, -31, -27, -25, -99,
        -25,  -8, -25,  -4,  -9, -14, -24, -29,
        -13,  -5,   5,   1,   0,  -5, -12, -20,
         -3,   3,  12,  11,  12,   7,  -1,  -9,
         -7,  -3,   8,   9,  11,   4,  -1, -12,
        -24, -13,  -6,   1,  -2,  -7, -14, -18,
        -37, -25, -23, -15, -24, -21, -32, -37,
        -50, -38, -31, -27, -24, -30, -38, -50
    ]
}

# Flip layout horizontally and vertically for Black
FLIP_SQUARE = [s ^ 56 for s in range(64)]

# ------------------------------------------------------------------------------
# THE EVALUATION ENGINE
# Calculates material imbalances, positional tables, pawn structure, and king safety
# ------------------------------------------------------------------------------

def evaluate_board(board: chess.Board) -> int:
    """Tapered Evaluation returning score relative to the side to move (White positive)."""
    mg_white, eg_white = 0, 0
    mg_black, eg_black = 0, 0
    game_phase = 0

    # Quick pre-calculations for piece types to speed up loop
    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if not piece:
            continue
        
        p_type = piece.piece_type
        p_color = piece.color

        # Sum phase weights to determine mid vs. endgame transitions
        if p_type == chess.KNIGHT:   game_phase += KNIGHT_PHASE
        elif p_type == chess.BISHOP: game_phase += BISHOP_PHASE
        elif p_type == chess.ROOK:   game_phase += ROOK_PHASE
        elif p_type == chess.QUEEN:  game_phase += QUEEN_PHASE

        if p_color == chess.WHITE:
            mg_white += MG_VALUES[p_type] + PST_MG[p_type][sq]
            eg_white += EG_VALUES[p_type] + PST_EG[p_type][sq]
            
            # Simple Pawn Structure Eval (White)
            if p_type == chess.PAWN:
                file = chess.square_file(sq)
                # Doubled Pawns penalty
                if len(white_pawns & chess.BB_FILES[file]) > 1:
                    mg_white -= 15
                    eg_white -= 20
                # Isolated Pawns penalty (no friendly pawns on adjacent files)
                adj_files = 0
                if file > 0: adj_files |= chess.BB_FILES[file - 1]
                if file < 7: adj_files |= chess.BB_FILES[file + 1]
                if not (white_pawns & adj_files):
                    mg_white -= 12
                    eg_white -= 16
        else:
            # Black positions are evaluated by mirroring the lookup indices
            flipped_sq = FLIP_SQUARE[sq]
            mg_black += MG_VALUES[p_type] + PST_MG[p_type][flipped_sq]
            eg_black += EG_VALUES[p_type] + PST_EG[p_type][flipped_sq]

            # Simple Pawn Structure Eval (Black)
            if p_type == chess.PAWN:
                file = chess.square_file(sq)
                if len(black_pawns & chess.BB_FILES[file]) > 1:
                    mg_black -= 15
                    eg_black -= 20
                adj_files = 0
                if file > 0: adj_files |= chess.BB_FILES[file - 1]
                if file < 7: adj_files |= chess.BB_FILES[file + 1]
                if not (black_pawns & adj_files):
                    mg_black -= 12
                    eg_black -= 16

    # Bishop Pair bonus
    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        mg_white += 30
        eg_white += 40
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        mg_black += 30
        eg_black += 40

    # Blend Middlegame and Endgame evaluations using the current Game Phase
    phase = min(game_phase, MAX_PHASE)
    mg_score = mg_white - mg_black
    eg_score = eg_white - eg_black
    
    final_eval = ((mg_score * phase) + (eg_score * (MAX_PHASE - phase))) // MAX_PHASE

    # Always return evaluation perspective relative to player whose turn it is
    return final_eval if board.turn == chess.WHITE else -final_eval

# ==============================================================================
# "RUTHLESS" - PART 2/2: ENGINE SEARCH SYSTEM AND UCI PROTOCOL
# ==============================================================================

# Search Constants
INFINITE_VAL = 1000000
MATE_THRESHOLD = 90000
MATE_SCORE_VAL = 99999

class TranspositionTable:
    """Highly optimized Transposition Table for caching previously calculated branches."""
    def __init__(self, max_size_mb=128):
        self.table = {}
        # Simple size limiting: roughly 128MB hash limits entries to ~2 million entries
        self.max_entries = (max_size_mb * 1024 * 1024) // 64

    def get(self, key):
        return self.table.get(key, None)

    def store(self, key, depth, score, flag, move, ply):
        if len(self.table) >= self.max_entries:
            self.table.clear()  # Save memory footprint when limit is reached
            
        # Adjust mate scores to be independent of search depth/ply
        if score > MATE_THRESHOLD:
            score += ply
        elif score < -MATE_THRESHOLD:
            score -= ply

        self.table[key] = {
            'depth': depth,
            'score': score,
            'flag': flag,
            'move': move
        }

    def retrieve_score(self, entry, ply):
        """Restore mate scores adjusted to the current depth level."""
        score = entry['score']
        if score > MATE_THRESHOLD:
            return score - ply
        elif score < -MATE_THRESHOLD:
            return score + ply
        return score


class RuthlessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.tt = TranspositionTable(max_size_mb=128)
        self.killer_moves = [[None] * 2 for _ in range(128)]
        self.history_scores = {}  # History heuristic score: history_scores[color][from_sq][to_sq]
        self.nodes_searched = 0
        self.stop_search = False
        self.start_time = 0.0
        self.time_limit = 10.0
        
        # Initialize history tables
        self.history_scores[chess.WHITE] = [[0] * 64 for _ in range(64)]
        self.history_scores[chess.BLACK] = [[0] * 64 for _ in range(64)]

    def clear_heuristics(self):
        self.killer_moves = [[None] * 2 for _ in range(128)]
        for color in (chess.WHITE, chess.BLACK):
            self.history_scores[color] = [[0] * 64 for _ in range(64)]

    def score_move(self, move, pv_move, ply):
        """Scores moves for ordering to optimize alpha-beta pruning."""
        if move == pv_move:
            return 1000000  # Priority 1: Principal Variation Move

        # Captures ordered using MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
        if self.board.is_capture(move):
            attacker = self.board.piece_at(move.from_square)
            target = self.board.piece_at(move.to_square)
            attacker_val = MG_VALUES[attacker.piece_type] if attacker else 100
            target_val = MG_VALUES[target.piece_type] if target else 100
            return 900000 + (target_val * 10 - attacker_val)

        # Promotions
        if move.promotion:
            return 800000 + MG_VALUES[move.promotion]

        # Killer Move Heuristic (quiet moves causing high beta-cutoffs in nearby branches)
        if ply < 128:
            if move == self.killer_moves[ply][0]:
                return 700000
            if move == self.killer_moves[ply][1]:
                return 650000

        # History Heuristic (quiet moves that historically perform well)
        color = self.board.turn
        h_score = self.history_scores[color][move.from_square][move.to_square]
        if h_score > 0:
            return min(600000, h_score)

        return 0

    def quiescence_search(self, alpha, beta):
        """Quiet selective search evaluating captures only, preventing tactical blindspots."""
        self.nodes_searched += 1
        
        if self.nodes_searched % 2048 == 0 and time.time() - self.start_time >= self.time_limit:
            self.stop_search = True
            return alpha

        stand_pat = evaluate_board(self.board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        captures = [m for m in self.board.generate_legal_moves() if self.board.is_capture(m)]
        captures.sort(key=lambda m: self.score_move(m, None, 0), reverse=True)

        for move in captures:
            self.board.push(move)
            score = -self.quiescence_search(-beta, -alpha)
            self.board.pop()

            if self.stop_search:
                return alpha

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def negamax(self, depth, alpha, beta, ply, allow_null=True):
        """Negamax Search featuring Alpha-Beta Pruning, NMP, LMR, and transposition checks."""
        self.nodes_searched += 1

        if self.nodes_searched % 2048 == 0 and time.time() - self.start_time >= self.time_limit:
            self.stop_search = True
            return alpha

        # 1. Base Game State & Draw Rules
        if self.board.is_checkmate():
            return -MATE_SCORE_VAL + ply
        if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():
            return 0

        if depth <= 0:
            return self.quiescence_search(alpha, beta)

        # 2. Transposition Table Probing
        zobrist_key = self.board.zobrist_hash()
        tt_entry = self.tt.get(zobrist_key)
        pv_move = None
        
        if tt_entry:
            pv_move = tt_entry['move']
            if tt_entry['depth'] >= depth:
                score = self.tt.retrieve_score(tt_entry, ply)
                if tt_entry['flag'] == 'EXACT':
                    return score
                elif tt_entry['flag'] == 'LOWER':
                    alpha = max(alpha, score)
                elif tt_entry['flag'] == 'UPPER':
                    beta = min(beta, score)
                if alpha >= beta:
                    return score

        in_check = self.board.is_check()

        # 3. Null Move Pruning (NMP)
        # Skip search branch if giving away a turn still yields a winning evaluation.
        if allow_null and not in_check and depth >= 3:
            # Only perform NMP if we have pieces other than pawns (avoiding zugzwang)
            major_pieces = (
                self.board.knights | self.board.bishops | self.board.rooks | self.board.queens
            ) & self.board.occupied_co[self.board.turn]
            
            if major_pieces:
                R = 3 if depth >= 6 else 2  # Adaptive reduction
                self.board.push_null()
                null_score = -self.negamax(depth - 1 - R, -beta, -beta + 1, ply + 1, allow_null=False)
                self.board.pop()
                
                if self.stop_search:
                    return alpha
                if null_score >= beta:
                    return beta

        # 4. Generate and Order Moves
        moves = list(self.board.generate_legal_moves())
        if not moves:
            if in_check:
                return -MATE_SCORE_VAL + ply
            return 0

        moves.sort(key=lambda m: self.score_move(m, pv_move, ply), reverse=True)

        best_score = -INFINITE_VAL
        best_move = None
        flag = 'UPPER'
        moves_searched = 0

        for move in moves:
            self.board.push(move)
            moves_searched += 1

            # 5. Late Move Reductions (LMR)
            # Quiet moves generated late in move-ordering are searched at reduced depth.
            if depth >= 3 and moves_searched > 4 and not in_check and not self.board.is_capture(move) and not move.promotion:
                reduction = 1
                if moves_searched > 12:
                    reduction = 2  # Reduce deeper for later non-tactical moves
                
                reduced_depth = max(1, depth - 1 - reduction)
                score = -self.negamax(reduced_depth, -alpha - 1, -alpha, ply + 1)
                
                # Re-search at full depth if reduced depth search returned a strong score
                if score > alpha and reduced_depth < depth - 1:
                    score = -self.negamax(depth - 1, -alpha - 1, -alpha, ply + 1)
            else:
                score = -self.negamax(depth - 1, -beta, -alpha, ply + 1)

            self.board.pop()

            if self.stop_search:
                return alpha

            if score > best_score:
                best_score = score
                best_move = move

            if score > alpha:
                alpha = score
                flag = 'EXACT'

            # 6. Beta Cutoff / Alpha-Beta Pruning
            if alpha >= beta:
                # Store dynamic heuristics for non-captures
                if not self.board.is_capture(move):
                    if ply < 128:
                        self.killer_moves[ply][1] = self.killer_moves[ply][0]
                        self.killer_moves[ply][0] = move
                    
                    # Log History Heuristic score scaling with depth
                    color = self.board.turn
                    self.history_scores[color][move.from_square][move.to_square] += depth * depth

                self.tt.store(zobrist_key, depth, beta, 'LOWER', move, ply)
                return beta

        self.tt.store(zobrist_key, depth, best_score, flag, best_move, ply)
        return best_score

    def search(self, depth_limit, time_limit):
        """Iterative Deepening harness wrapped in an Aspiration Window search wrapper."""
        self.start_time = time.time()
        self.time_limit = max(0.02, time_limit)
        self.stop_search = False
        self.nodes_searched = 0

        legal_moves = list(self.board.generate_legal_moves())
        if not legal_moves:
            return None
            
        best_move = legal_moves[0]
        last_completed_score = 0

        # Iterative Deepening
        for current_depth in range(1, depth_limit + 1):
            
            # Use Aspiration Windows for searches deeper than 3
            if current_depth >= 4:
                window = 40  # Centipawn window range around previous depth score
                alpha = last_completed_score - window
                beta = last_completed_score + window
            else:
                alpha = -INFINITE_VAL
                beta = INFINITE_VAL

            while True:
                z_key = chess.polyglot.zobrist_hash(self.board)
                tt_entry = self.tt.get(z_key)
                pv_move = tt_entry['move'] if tt_entry else None

                moves = list(self.board.generate_legal_moves())
                moves.sort(key=lambda m: self.score_move(m, pv_move, 0), reverse=True)

                best_score = -INFINITE_VAL
                iter_best_move = None

                for move in moves:
                    self.board.push(move)
                    score = -self.negamax(current_depth - 1, -beta, -alpha, 1)
                    self.board.pop()

                    if self.stop_search:
                        break

                    if score > best_score:
                        best_score = score
                        iter_best_move = move
                    
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break

                if self.stop_search:
                    break

                # Adjust window boundaries if score falls outside expectations
                if best_score <= alpha or best_score >= beta:
                    alpha = -INFINITE_VAL
                    beta = INFINITE_VAL
                    continue  # Re-search window with infinite boundaries
                else:
                    last_completed_score = best_score
                    break

            if not self.stop_search and iter_best_move:
                best_move = iter_best_move
                score_str = f"cp {best_score}" if abs(best_score) < MATE_THRESHOLD else f"mate {int((MATE_SCORE_VAL - abs(best_score)) / 2) + 1}"
                print(f"info depth {current_depth} score {score_str} nodes {self.nodes_searched} time {int((time.time() - self.start_time) * 1000)} pv {best_move.uci()}", flush=True)

            # Safety break if we spent too much time on the last completed depth
            if time.time() - self.start_time >= self.time_limit:
                break

        return best_move

# ==============================================================================
# UCI LOOP IMPLEMENTATION
# ==============================================================================

def main():
    engine = RuthlessEngine()

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue

            tokens = line.split()
            cmd = tokens[0]

            if cmd == "uci":
                print("id name Ruthless v2.0", flush=True)
                print("id author Claude", flush=True)
                print("uciok", flush=True)

            elif cmd == "isready":
                print("readyok", flush=True)

            elif cmd == "ucinewgame":
                engine.board = chess.Board()
                engine.tt.table.clear()
                engine.clear_heuristics()

            elif cmd == "position":
                if len(tokens) > 1 and tokens[1] == "startpos":
                    engine.board = chess.Board()
                    moves_idx = 2
                elif len(tokens) > 1 and tokens[1] == "fen":
                    fen_parts = []
                    idx = 2
                    while idx < len(tokens) and tokens[idx] != "moves":
                        fen_parts.append(tokens[idx])
                        idx += 1
                    engine.board = chess.Board(" ".join(fen_parts))
                    moves_idx = idx

                if moves_idx < len(tokens) and tokens[moves_idx] == "moves":
                    for move_str in tokens[moves_idx + 1:]:
                        try:
                            move = chess.Move.from_uci(move_str)
                            if move in engine.board.legal_moves:
                                engine.board.push(move)
                        except ValueError:
                            pass

            elif cmd == "go":
                wtime = btime = winc = binc = None
                movetime = None
                depth_limit = 20  # Max default search depth

                for i in range(1, len(tokens), 2):
                    if i + 1 >= len(tokens):
                        break
                    param = tokens[i]
                    val = tokens[i+1]

                    if param == "wtime": wtime = int(val)
                    elif param == "btime": btime = int(val)
                    elif param == "winc": winc = int(val)
                    elif param == "binc": binc = int(val)
                    elif param == "movetime": movetime = int(val)
                    elif param == "depth": depth_limit = int(val)

                # Advanced Time Manager
                search_time = 3.0  # Safe default fallback time
                if movetime is not None:
                    search_time = (movetime / 1000.0) * 0.95
                else:
                    my_time = wtime if engine.board.turn == chess.WHITE else btime
                    my_inc = winc if engine.board.turn == chess.WHITE else binc
                    
                    if my_time is not None:
                        my_inc = my_inc or 0
                        # Determine base move allocation (targeting roughly 40-move matches)
                        base_allocation = my_time / 40.0
                        # Calculate incremental offset
                        inc_allocation = my_inc * 0.75
                        search_time = (base_allocation + inc_allocation) / 1000.0
                        
                        # Add a strict buffer so we never timeout during hyper-blitz or bullet
                        search_time = max(0.015, min(search_time, (my_time * 0.4) / 1000.0))

                best_move = engine.search(depth_limit=depth_limit, time_limit=search_time)
                if best_move:
                    print(f"bestmove {best_move.uci()}", flush=True)
                else:
                    legal = list(engine.board.generate_legal_moves())
                    if legal:
                        print(f"bestmove {legal[0].uci()}", flush=True)
                    else:
                        print("bestmove 0000", flush=True)

            elif cmd == "quit":
                break

        except Exception as e:
            sys.stderr.write(f"Exception in UCI Loop: {str(e)}\n")
            sys.stderr.flush()

if __name__ == "__main__":
    main()