#####Creator: Dr.flatpawn
import sys
import time
import chess
import chess.polyglot
import random

PAWN_PHASE   = 0
KNIGHT_PHASE = 1
BISHOP_PHASE = 1
ROOK_PHASE   = 2
QUEEN_PHASE  = 4
MAX_PHASE    = 24 
PASSED_PAWN_MG = [0, 5, 12, 25, 45, 70, 110, 0]
PASSED_PAWN_EG = [0, 10, 25, 45, 70, 120, 180, 0]
KNIGHT_MOBILITY = 4
BISHOP_MOBILITY = 5
ROOK_MOBILITY = 2
QUEEN_MOBILITY = 1
ROOK_OPEN_FILE_MG = 22
ROOK_OPEN_FILE_EG = 18
ROOK_SEMIOPEN_FILE_MG = 12
ROOK_SEMIOPEN_FILE_EG = 10
MAX_HISTORY = 16384

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

PAWN_TABLE_MG = [
    0,   0,   0,   0,   0,   0,   0,   0,
   -3,  -1,   3, -11, -11,   3,  -1,  -3,
   -6,  -2,   2,  -4,  -4,   2,  -2,  -6,
   -5,   0,   5,   9,   9,   5,   0,  -5,
    1,   6,  11,  21,  21,  11,   6,   1,
   12,  17,  22,  32,  32,  22,  17,  12,
   25,  30,  35,  45,  45,  35,  30,  25,
    0,   0,   0,   0,   0,   0,   0,   0
]

PAWN_TABLE_EG = [
    0,   0,   0,   0,   0,   0,   0,   0,
   -6,  -4,  -2,   1,   1,  -2,  -4,  -6,
   -5,  -3,  -1,   3,   3,  -1,  -3,  -5,
   -3,  -1,   2,   6,   6,   2,  -1,  -3,
    0,   2,   5,   9,   9,   5,   2,   0,
    4,   6,   9,  13,  13,   9,   6,   4,
    9,  11,  14,  18,  18,  14,  11,   9,
    0,   0,   0,   0,   0,   0,   0,   0
]

KNIGHT_TABLE_MG = [
  -165, -100,  -73,  -62,  -62,  -73, -100, -165,
  -106,  -51,  -22,  -11,  -11,  -22,  -51, -106,
   -73,  -20,    7,   17,   17,    7,  -20,  -73,
   -56,   -5,   20,   31,   31,   20,   -5,  -56,
   -49,    1,   25,   36,   36,   25,    1,  -49,
   -56,   -4,   19,   30,   30,   19,   -4,  -56,
   -81,  -34,  -10,    0,    0,  -10,  -34,  -81,
  -128,  -75,  -50,  -39,  -39,  -50,  -75, -128
]

KNIGHT_TABLE_EG = [
   -68,  -45,  -35,  -30,  -30,  -35,  -45,  -68,
   -45,  -24,  -13,   -8,   -8,  -13,  -24,  -45,
   -34,  -13,   -3,    2,    2,   -3,  -13,  -34,
   -28,   -7,    3,    8,    8,    3,   -7,  -28,
   -27,   -6,    4,    9,    9,    4,   -6,  -27,
   -31,  -11,   -1,    4,    4,   -1,  -11,  -31,
   -46,  -26,  -16,  -11,  -11,  -16,  -26,  -46,
   -68,  -48,  -38,  -33,  -33,  -38,  -48,  -68
]

BISHOP_TABLE_MG = [
   -38,  -20,  -18,  -16,  -16,  -18,  -20,  -38,
   -18,    1,    3,    5,    5,    3,    1,  -18,
   -14,    4,    7,   10,   10,    7,    4,  -14,
   -12,    6,    9,   13,   13,    9,    6,  -12,
   -12,    5,    9,   12,   12,    9,    5,  -12,
   -14,    3,    7,   10,   10,    7,    3,  -14,
   -19,   -1,    2,    4,    4,    2,   -1,  -19,
   -35,  -18,  -16,  -14,  -14,  -16,  -18,  -35
]

BISHOP_TABLE_EG = [
   -23,  -13,  -11,  -10,  -10,  -11,  -13,  -23,
   -13,   -3,   -2,    0,    0,   -2,   -3,  -13,
   -11,   -1,    0,    2,    2,    0,   -1,  -11,
   -10,    0,    2,    4,    4,    2,    0,  -10,
    -9,    0,    2,    4,    4,    2,    0,   -9,
   -11,   -1,    0,    2,    2,    0,   -1,  -11,
   -14,   -4,   -2,    0,    0,   -2,   -4,  -14,
   -23,  -14,  -12,  -11,  -11,  -12,  -14,  -23
]

ROOK_TABLE_MG = [
   -15,   -7,  -11,   -5,   -5,  -11,   -7,  -15,
   -14,   -6,  -10,   -4,   -4,  -10,   -6,  -14,
   -15,   -7,  -11,   -5,   -5,  -11,   -7,  -15,
   -17,   -9,  -13,   -7,   -7,  -13,   -9,  -17,
   -18,  -10,  -14,   -8,   -8,  -14,  -10,  -18,
   -16,   -8,  -12,   -6,   -6,  -12,   -8,  -16,
    -4,    4,    0,    6,    6,    0,    4,   -4,
   -14,   -6,  -10,   -4,   -4,  -10,   -6,  -14
]

ROOK_TABLE_EG = [
   -19,  -13,  -15,  -11,  -11,  -15,  -13,  -19,
   -15,   -9,  -11,   -7,   -7,  -11,   -9,  -15,
   -13,   -7,   -9,   -5,   -5,   -9,   -7,  -13,
   -11,   -5,   -7,   -3,   -3,   -7,   -5,  -11,
   -11,   -5,   -7,   -3,   -3,   -7,   -5,  -11,
   -12,   -6,   -8,   -4,   -4,   -8,   -6,  -12,
   -12,   -6,   -8,   -4,   -4,   -8,   -6,  -12,
   -18,  -12,  -14,  -10,  -10,  -14,  -12,  -18
]

QUEEN_TABLE_MG = [
    -7,   -3,   -5,   -2,   -2,   -5,   -3,   -7,
    -5,    0,   -2,    1,    1,   -2,    0,   -5,
    -5,   -1,   -2,    0,    0,   -2,   -1,   -5,
    -6,   -2,   -3,   -1,   -1,   -3,   -2,   -6,
    -4,    0,   -1,    1,    1,   -1,    0,   -4,
    -5,   -1,   -2,    0,    0,   -2,   -1,   -5,
    -6,   -2,   -3,   -1,   -1,   -3,   -2,   -6,
    -7,   -3,   -5,   -2,   -2,   -5,   -3,   -7
]

QUEEN_TABLE_EG = [
   -23,  -14,  -17,  -12,  -12,  -17,  -14,  -23,
   -16,   -8,  -11,   -6,   -6,  -11,   -8,  -16,
   -13,   -5,   -8,   -3,   -3,   -8,   -5,  -13,
   -11,   -3,   -6,   -1,   -1,   -6,   -3,  -11,
   -11,   -3,   -6,   -1,   -1,   -6,   -3,  -11,
   -13,   -5,   -8,   -3,   -3,   -8,   -5,  -13,
   -16,   -8,  -11,   -6,   -6,  -11,   -8,  -16,
   -22,  -14,  -17,  -12,  -12,  -17,  -14,  -22
]

KING_TABLE_MG = [
    30,   45,   15,    0,    0,   15,   45,   30,
    15,   30,    0,  -15,  -15,    0,   30,   15,
   -15,    0,  -30,  -45,  -45,  -30,    0,  -15,
   -30,  -15,  -45,  -60,  -60,  -45,  -15,  -30,
   -45,  -30,  -60,  -75,  -75,  -60,  -30,  -45,
   -60,  -45,  -75,  -90,  -90,  -75,  -45,  -60,
   -75,  -60,  -90, -105, -105,  -90,  -60,  -75,
   -90,  -75, -105, -120, -120, -105,  -75,  -90
]

KING_TABLE_EG = [
   -102,  -68,  -53,  -46,  -46,  -53,  -68, -102,
    -66,  -34,  -20,  -13,  -13,  -20,  -34,  -66,
    -48,  -17,   -4,    2,    2,   -4,  -17,  -48,
    -38,   -8,    5,   11,   11,    5,   -8,  -38,
    -34,   -5,    8,   14,   14,    8,   -5,  -34,
    -36,   -7,    5,   11,   11,    5,   -7,  -36,
    -49,  -19,   -6,    0,    0,   -6,  -19,  -49,
    -73,  -42,  -29,  -22,  -22,  -29,  -42,  -73
]

FLIP_TABLE = [
    56,  57,  58,  59,  60,  61,  62,  63,
    48,  49,  50,  51,  52,  53,  54,  55,
    40,  41,  42,  43,  44,  45,  46,  47,
    32,  33,  34,  35,  36,  37,  38,  39,
    24,  25,  26,  27,  28,  29,  30,  31,
    16,  17,  18,  19,  20,  21,  22,  23,
     8,   9,  10,  11,  12,  13,  14,  15,
     0,   1,   2,   3,   4,   5,   6,   7
]

INFINITE_VAL = 32000
MATE_SCORE_VAL = 30000
MATE_THRESHOLD = 29000

MVV_LVA = [
    [10, 11, 12, 13, 14, 15], 
    [20, 21, 22, 23, 24, 25], 
    [30, 31, 32, 33, 34, 35], 
    [40, 41, 42, 43, 44, 45], 
    [50, 51, 52, 53, 54, 55], 
    [0,   0,  0,  0,  0,  0],  
]

def get_pstw_index(square, color):
    return FLIP_TABLE[square] if color == chess.BLACK else square

class SimpleTranspositionTable:
    def __init__(self, size_mb=16):
        self.entry_size = 32  
        self.num_entries = (size_mb * 1024 * 1024) // self.entry_size
        self.table = {}

    def clear(self):
        self.table.clear()

    def store(self, key, depth, score, flag, move):
        slot = key % self.num_entries
        self.table[slot] = {
            'key': key,
            'depth': depth,
            'score': score,
            'flag': flag,
            'move': move
        }

    def get(self, key):
        slot = key % self.num_entries
        entry = self.table.get(slot)
        if entry and entry['key'] == key:
            return entry
        return None

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.tt = SimpleTranspositionTable(size_mb=16)
        self.history_table = [[0] * 64 for _ in range(2)] 
        self.killer_moves = [[None] * 2 for _ in range(128)]
        self.nodes_searched = 0
        self.start_time = 0.0
        self.time_limit = 0.0
        self.stop_search = False

    def evaluate(self):
        mg_white = 0
        mg_black = 0
        eg_white = 0
        eg_black = 0
        phase = 0

        w_pawns = self.board.pieces(chess.PAWN, chess.WHITE)
        b_pawns = self.board.pieces(chess.PAWN, chess.BLACK)

        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if not piece:
                continue

            p_type = piece.piece_type
            color = piece.color

            if p_type == chess.PAWN:
                phase += PAWN_PHASE
                if color == chess.WHITE:
                    mg_white += MG_VALUES[chess.PAWN] + PAWN_TABLE_MG[get_pstw_index(sq, chess.WHITE)]
                    eg_white += EG_VALUES[chess.PAWN] + PAWN_TABLE_EG[get_pstw_index(sq, chess.WHITE)]
                else:
                    mg_black += MG_VALUES[chess.PAWN] + PAWN_TABLE_MG[get_pstw_index(sq, chess.BLACK)]
                    eg_black += EG_VALUES[chess.PAWN] + PAWN_TABLE_EG[get_pstw_index(sq, chess.BLACK)]

            elif p_type == chess.KNIGHT:
                phase += KNIGHT_PHASE
                bb = chess.BB_SQUARES[sq]
                attacks = chess.BB_KNIGHT_ATTACKS[sq]
                mobility = bin(attacks & ~self.board.occupied_co[color]).count("1")
                mobility_bonus = mobility * KNIGHT_MOBILITY

                if color == chess.WHITE:
                    mg_white += MG_VALUES[chess.KNIGHT] + KNIGHT_TABLE_MG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus
                    eg_white += EG_VALUES[chess.KNIGHT] + KNIGHT_TABLE_EG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus
                else:
                    mg_black += MG_VALUES[chess.KNIGHT] + KNIGHT_TABLE_MG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus
                    eg_black += EG_VALUES[chess.KNIGHT] + KNIGHT_TABLE_EG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus

            elif p_type == chess.BISHOP:
                phase += BISHOP_PHASE
                mobility = len(self.board.attacks(sq))
                mobility_bonus = mobility * BISHOP_MOBILITY

                if color == chess.WHITE:
                    mg_white += MG_VALUES[chess.BISHOP] + BISHOP_TABLE_MG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus
                    eg_white += EG_VALUES[chess.BISHOP] + BISHOP_TABLE_EG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus
                else:
                    mg_black += MG_VALUES[chess.BISHOP] + BISHOP_TABLE_MG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus
                    eg_black += EG_VALUES[chess.BISHOP] + BISHOP_TABLE_EG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus

            elif p_type == chess.ROOK:
                phase += ROOK_PHASE
                mobility = len(self.board.attacks(sq))
                mobility_bonus = mobility * ROOK_MOBILITY

                file_idx = chess.square_file(sq)
                w_pawn_on_file = bool(w_pawns & chess.BB_FILES[file_idx])
                b_pawn_on_file = bool(b_pawns & chess.BB_FILES[file_idx])

                file_bonus_mg = 0
                file_bonus_eg = 0
                if not w_pawn_on_file and not b_pawn_on_file:
                    file_bonus_mg = ROOK_OPEN_FILE_MG
                    file_bonus_eg = ROOK_OPEN_FILE_EG
                elif (color == chess.WHITE and not w_pawn_on_file) or (color == chess.BLACK and not b_pawn_on_file):
                    file_bonus_mg = ROOK_SEMIOPEN_FILE_MG
                    file_bonus_eg = ROOK_SEMIOPEN_FILE_EG

                if color == chess.WHITE:
                    mg_white += MG_VALUES[chess.ROOK] + ROOK_TABLE_MG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus + file_bonus_mg
                    eg_white += EG_VALUES[chess.ROOK] + ROOK_TABLE_EG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus + file_bonus_eg
                else:
                    mg_black += MG_VALUES[chess.ROOK] + ROOK_TABLE_MG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus + file_bonus_mg
                    eg_black += EG_VALUES[chess.ROOK] + ROOK_TABLE_EG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus + file_bonus_eg

            elif p_type == chess.QUEEN:
                phase += QUEEN_PHASE
                mobility = len(self.board.attacks(sq))
                mobility_bonus = mobility * QUEEN_MOBILITY

                if color == chess.WHITE:
                    mg_white += MG_VALUES[chess.QUEEN] + QUEEN_TABLE_MG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus
                    eg_white += EG_VALUES[chess.QUEEN] + QUEEN_TABLE_EG[get_pstw_index(sq, chess.WHITE)] + mobility_bonus
                else:
                    mg_black += MG_VALUES[chess.QUEEN] + QUEEN_TABLE_MG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus
                    eg_black += EG_VALUES[chess.QUEEN] + QUEEN_TABLE_EG[get_pstw_index(sq, chess.BLACK)] + mobility_bonus

            elif p_type == chess.KING:
                if color == chess.WHITE:
                    mg_white += KING_TABLE_MG[get_pstw_index(sq, chess.WHITE)]
                    eg_white += KING_TABLE_EG[get_pstw_index(sq, chess.WHITE)]
                else:
                    mg_black += KING_TABLE_MG[get_pstw_index(sq, chess.BLACK)]
                    eg_black += KING_TABLE_EG[get_pstw_index(sq, chess.BLACK)]

        if len(self.board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
            mg_white += 30
            eg_white += 40
        if len(self.board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
            mg_black += 30
            eg_black += 40

        for sq in w_pawns:
            file_idx = chess.square_file(sq)
            rank_idx = chess.square_rank(sq)
            passed = True
            for r in range(rank_idx + 1, 7):
                squares_to_check = [chess.square(file_idx, r)]
                if file_idx > 0: squares_to_check.append(chess.square(file_idx - 1, r))
                if file_idx < 7: squares_to_check.append(chess.square(file_idx + 1, r))
                if any(self.board.piece_at(s) == chess.Piece(chess.PAWN, chess.BLACK) for s in squares_to_check):
                    passed = False
                    break
            if passed:
                mg_white += PASSED_PAWN_MG[rank_idx]
                eg_white += PASSED_PAWN_EG[rank_idx]

        for sq in b_pawns:
            file_idx = chess.square_file(sq)
            rank_idx = chess.square_rank(sq)
            passed = True
            for r in range(1, rank_idx):
                squares_to_check = [chess.square(file_idx, r)]
                if file_idx > 0: squares_to_check.append(chess.square(file_idx - 1, r))
                if file_idx < 7: squares_to_check.append(chess.square(file_idx + 1, r))
                if any(self.board.piece_at(s) == chess.Piece(chess.PAWN, chess.WHITE) for s in squares_to_check):
                    passed = False
                    break
            if passed:
                mg_black += PASSED_PAWN_MG[7 - rank_idx]
                eg_black += PASSED_PAWN_EG[7 - rank_idx]

        mg_score = mg_white - mg_black
        eg_score = eg_white - eg_black

        p = min(phase, MAX_PHASE)
        total_score = (mg_score * p + eg_score * (MAX_PHASE - p)) // MAX_PHASE

        return total_score if self.board.turn == chess.WHITE else -total_score

    def score_move(self, move, pv_move, depth_from_root):
        if pv_move and move == pv_move:
            return 100000

        if self.board.is_capture(move):
            attacker = self.board.piece_at(move.from_square)
            target = self.board.piece_at(move.to_square)
            if attacker and target:
                return 90000 + MVV_LVA[target.piece_type - 1][attacker.piece_type - 1]
            elif self.board.is_en_passant(move):
                return 90010
            return 90000

        if move == self.killer_moves[depth_from_root][0]:
            return 40000
        if move == self.killer_moves[depth_from_root][1]:
            return 35000

        color_idx = 1 if self.board.turn == chess.WHITE else 0
        return self.history_table[color_idx][move.to_square]

    def quiescence(self, alpha, beta):
        self.nodes_searched += 1

        if self.nodes_searched % 2048 == 0:
            if time.time() - self.start_time >= self.time_limit:
                self.stop_search = True
                return alpha

        stand_pat = self.evaluate()
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        moves = [m for m in self.board.generate_legal_moves() if self.board.is_capture(m)]
        moves.sort(key=lambda m: self.score_move(m, None, 0), reverse=True)

        for move in moves:
            self.board.push(move)
            score = -self.quiescence(-beta, -alpha)
            self.board.pop()

            if self.stop_search:
                return alpha

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def negamax(self, depth, alpha, beta, depth_from_root):
        self.nodes_searched += 1

        if self.nodes_searched % 2048 == 0:
            if time.time() - self.start_time >= self.time_limit:
                self.stop_search = True
                return alpha

        if self.board.is_repetition(2) or self.board.is_fifty_moves():
            return 0

        z_key = chess.polyglot.zobrist_hash(self.board)
        tt_entry = self.tt.get(z_key)
        if tt_entry and tt_entry['depth'] >= depth:
            if tt_entry['flag'] == 'EXACT':
                return tt_entry['score']
            elif tt_entry['flag'] == 'LOWERBOUND' and tt_entry['score'] >= beta:
                return beta
            elif tt_entry['flag'] == 'UPPERBOUND' and tt_entry['score'] <= alpha:
                return alpha

        if depth <= 0:
            return self.quiescence(alpha, beta)

        if not self.board.is_check() and depth >= 3:
            R = 2 if depth < 7 else 3
            self.board.push_穩定() if hasattr(self.board, 'push_穩定') else self.board.push(chess.Move.null())
            null_score = -self.negamax(depth - 1 - R, -beta, -beta + 1, depth_from_root + 1)
            self.board.pop()
            if self.stop_search:
                return alpha
            if null_score >= beta:
                return beta

        pv_move = tt_entry['move'] if tt_entry else None
        moves = list(self.board.generate_legal_moves())

        if not moves:
            if self.board.is_check():
                return -MATE_SCORE_VAL + depth_from_root
            return 0

        moves.sort(key=lambda m: self.score_move(m, pv_move, depth_from_root), reverse=True)

        best_score = -INFINITE_VAL
        best_move_this_node = None
        moves_searched_count = 0

        for move in moves:
            self.board.push(move)
            moves_searched_count += 1

            if moves_searched_count > 4 and depth >= 3 and not self.board.is_check() and not self.board.is_capture(move):
                score = -self.negamax(depth - 2, -alpha - 1, -alpha, depth_from_root + 1)
                if score > alpha:
                    score = -self.negamax(depth - 1, -beta, -alpha, depth_from_root + 1)
            else:
                score = -self.negamax(depth - 1, -beta, -alpha, depth_from_root + 1)

            self.board.pop()

            if self.stop_search:
                return alpha

            if score > best_score:
                best_score = score
                best_move_this_node = move

            alpha = max(alpha, score)
            if alpha >= beta:
                if not self.board.is_capture(move):
                    color_idx = 1 if self.board.turn == chess.WHITE else 0
                    self.history_table[color_idx][move.to_square] += depth * depth
                    if self.history_table[color_idx][move.to_square] > MAX_HISTORY:
                        for s in range(64):
                            self.history_table[color_idx][s] //= 2

                    if move != self.killer_moves[depth_from_root][0]:
                        self.killer_moves[depth_from_root][1] = self.killer_moves[depth_from_root][0]
                        self.killer_moves[depth_from_root][0] = move
                break

        if self.stop_search:
            return alpha

        tt_flag = 'EXACT'
        if best_score <= alpha:
            tt_flag = 'UPPERBOUND'
        elif best_score >= beta:
            tt_flag = 'LOWERBOUND'

        self.tt.store(z_key, depth, best_score, tt_flag, best_move_this_node)
        return best_score

    def search(self, depth_limit, time_limit):
        self.start_time = time.time()
        self.time_limit = max(0.015, time_limit)
        self.stop_search = False
        self.nodes_searched = 0

        legal_moves = list(self.board.generate_legal_moves())
        if not legal_moves:
            return None

        # Coup de secours instantané si crash de gestion du temps
        best_move = legal_moves[0]
        last_completed_score = 0

        for current_depth in range(1, depth_limit + 1):
            if time.time() - self.start_time >= self.time_limit:
                break

            if current_depth >= 4:
                window = 40
                alpha = last_completed_score - window
                beta = last_completed_score + window
            else:
                alpha = -INFINITE_VAL
                beta = INFINITE_VAL

            alpha_original = alpha
            beta_original = beta

            while True:
                if time.time() - self.start_time >= self.time_limit:
                    self.stop_search = True
                    break

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

                if best_score <= alpha_original:
                    alpha = -INFINITE_VAL
                    beta = INFINITE_VAL
                    alpha_original = -INFINITE_VAL
                    beta_original = INFINITE_VAL
                    continue
                elif best_score >= beta_original:
                    alpha = -INFINITE_VAL
                    beta = INFINITE_VAL
                    alpha_original = -INFINITE_VAL
                    beta_original = INFINITE_VAL
                    continue
                else:
                    last_completed_score = best_score
                    break

            # CORRECTION : On extrait le meilleur coup même si la recherche a été coupée
            if iter_best_move:
                best_move = iter_best_move

            if not self.stop_search and iter_best_move:
                score_str = f"cp {best_score}" if abs(best_score) < MATE_THRESHOLD else f"mate {int((MATE_SCORE_VAL - abs(best_score)) / 2) + 1}"
                print(f"info depth {current_depth} score {score_str} nodes {self.nodes_searched} time {int((time.time() - self.start_time) * 1000)} pv {best_move.uci()}", flush=True)

            if time.time() - self.start_time >= self.time_limit:
                break

        return best_move

def main():
    engine = ChessEngine()
    depth_limit = 64

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            tokens = line.split()
            if not tokens:
                continue

            cmd = tokens[0]

            if cmd == "uci":
                print("id name Ruthless V2.1")
                print("id author YourName")
                print("uciok", flush=True)

            elif cmd == "isready":
                print("readyok", flush=True)

            elif cmd == "ucinewgame":
                engine.tt.clear()
                engine.history_table = [[0] * 64 for _ in range(2)]
                engine.killer_moves = [[None] * 2 for _ in range(128)]
                engine.board = chess.Board()

            elif cmd == "position":
                if len(tokens) >= 2 and tokens[1] == "startpos":
                    engine.board = chess.Board()
                    if "moves" in tokens:
                        move_idx = tokens.index("moves")
                        for m_str in tokens[move_idx + 1:]:
                            engine.board.push_uci(m_str)
                elif len(tokens) >= 2 and tokens[1] == "fen":
                    fen_parts = []
                    idx = 2
                    while idx < len(tokens) and tokens[idx] != "moves":
                        fen_parts.append(tokens[idx])
                        idx += 1
                    fen_str = " ".join(fen_parts)
                    engine.board = chess.Board(fen_str)
                    if idx < len(tokens) and tokens[idx] == "moves":
                        for m_str in tokens[idx + 1:]:
                            engine.board.push_uci(m_str)

            elif cmd == "go":
                wtime = None
                btime = None
                winc = None
                binc = None
                movetime = None

                for i in range(1, len(tokens) - 1, 2):
                    param = tokens[i]
                    val_str = tokens[i+1]
                    try:
                        val = int(val_str)
                    except ValueError:
                        continue

                    if param == "wtime": wtime = val
                    elif param == "btime": btime = val
                    elif param == "winc": winc = val
                    elif param == "binc": binc = val
                    elif param == "movetime": movetime = val

                search_time = 3.0  
                if movetime is not None:
                    search_time = (movetime / 1000.0) * 0.95
                else:
                    my_time = wtime if engine.board.turn == chess.WHITE else btime
                    my_inc = winc if engine.board.turn == chess.WHITE else binc
                    
                    if my_time is not None:
                        my_inc = my_inc or 0
                        base_allocation = my_time / 40.0
                        inc_allocation = my_inc * 0.75
                        search_time = (base_allocation + inc_allocation) / 1000.0
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
            sys.stderr.write(f"Exception: {str(e)}\n")
            sys.stderr.flush()
            break

if __name__ == "__main__":
    main()
# ==============================================================================
#  RUTHLESS Chess Engine
#  Copyright (c) 2026 Dr.Flatpawn
#
#  This project is released under the MIT License.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#
#  Author: Dr.Flatpawn
#  Project: Ruthless Chess Engine
#  Repository: https://github.com/DrFlatpawn/Ruthless
# ==============================================================================
