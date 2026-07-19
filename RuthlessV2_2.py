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
        -50, -30, -30, -30, -30, -30, -30, -50,
        -30, -30,   0,   0,   0,   0, -30, -30,
        -30, -10,  20,  30,  30,  20, -10, -30,
        -30, -10,  30,  40,  40,  30, -10, -30,
        -30, -10,  30,  40,  40,  30, -10, -30,
        -30, -10,  20,  30,  30,  20, -10, -30,
        -30, -20, -10,   0,   0, -10, -20, -30,
        -50, -40, -30, -20, -20, -30, -40, -50
    ]
}

FLIP_SQUARE = [s ^ 56 for s in range(64)]


MOBILITY_MG = {chess.KNIGHT: 4, chess.BISHOP: 4, chess.ROOK: 2, chess.QUEEN: 1}
MOBILITY_EG = {chess.KNIGHT: 4, chess.BISHOP: 4, chess.ROOK: 3, chess.QUEEN: 2}

PASSED_PAWN_MG = [0, 5, 10, 20, 35, 60, 100, 0]   
PASSED_PAWN_EG = [0, 10, 20, 40, 70, 120, 200, 0]

ROOK_OPEN_FILE_MG = 20
ROOK_OPEN_FILE_EG = 10
ROOK_SEMI_OPEN_MG = 10
ROOK_SEMI_OPEN_EG = 5

KING_OPEN_FILE_PENALTY_MG = 10
KING_SHIELD_PENALTY_MG = 8

TEMPO_BONUS = 12


def _is_passed_pawn(file, rank, color, enemy_pawn_squares):
    lo = max(0, file - 1)
    hi = min(7, file + 1)
    for esq in enemy_pawn_squares:
        ef = chess.square_file(esq)
        if lo <= ef <= hi:
            er = chess.square_rank(esq)
            if color == chess.WHITE and er > rank:
                return False
            if color == chess.BLACK and er < rank:
                return False
    return True


def _king_shield_penalty(king_sq, own_pawns_bb, color):
    
    kf = chess.square_file(king_sq)
    kr = chess.square_rank(king_sq)
    forward = 1 if color == chess.WHITE else -1
    penalty = 0
    for f in range(max(0, kf - 1), min(7, kf + 1) + 1):
        found = False
        for dist in (1, 2):
            r = kr + forward * dist
            if 0 <= r <= 7:
                sq = chess.square(f, r)
                if own_pawns_bb & chess.BB_SQUARES[sq]:
                    found = True
                    break
        if not found:
            penalty += 1
    return penalty


def evaluate_board(board: chess.Board) -> int:

    mg_white, eg_white = 0, 0
    mg_black, eg_black = 0, 0
    game_phase = 0

    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    white_pawn_list = list(white_pawns)
    black_pawn_list = list(black_pawns)

    white_has_queen = bool(board.pieces(chess.QUEEN, chess.WHITE))
    black_has_queen = bool(board.pieces(chess.QUEEN, chess.BLACK))

    white_king_sq = board.king(chess.WHITE)
    black_king_sq = board.king(chess.BLACK)

    white_pawn_attacks = 0
    for psq in white_pawn_list:
        white_pawn_attacks |= chess.BB_PAWN_ATTACKS[chess.WHITE][psq]
    black_pawn_attacks = 0
    for psq in black_pawn_list:
        black_pawn_attacks |= chess.BB_PAWN_ATTACKS[chess.BLACK][psq]

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if not piece:
            continue

        p_type = piece.piece_type
        p_color = piece.color

        if p_type == chess.KNIGHT:   game_phase += KNIGHT_PHASE
        elif p_type == chess.BISHOP: game_phase += BISHOP_PHASE
        elif p_type == chess.ROOK:   game_phase += ROOK_PHASE
        elif p_type == chess.QUEEN:  game_phase += QUEEN_PHASE

        if p_color == chess.WHITE:
            mg_white += MG_VALUES[p_type] + PST_MG[p_type][sq]
            eg_white += EG_VALUES[p_type] + PST_EG[p_type][sq]

            if p_type == chess.PAWN:
                file = chess.square_file(sq)
                rank = chess.square_rank(sq)

                if len(white_pawns & chess.BB_FILES[file]) > 1:
                    mg_white -= 15
                    eg_white -= 20

                adj_files = 0
                if file > 0: adj_files |= chess.BB_FILES[file - 1]
                if file < 7: adj_files |= chess.BB_FILES[file + 1]
                if not (white_pawns & adj_files):
                    mg_white -= 12
                    eg_white -= 16

                if _is_passed_pawn(file, rank, chess.WHITE, black_pawn_list):
                    mg_white += PASSED_PAWN_MG[rank]
                    eg_white += PASSED_PAWN_EG[rank]

            elif p_type == chess.ROOK:
                file = chess.square_file(sq)
                own_on_file = white_pawns & chess.BB_FILES[file]
                enemy_on_file = black_pawns & chess.BB_FILES[file]
                if not own_on_file and not enemy_on_file:
                    mg_white += ROOK_OPEN_FILE_MG
                    eg_white += ROOK_OPEN_FILE_EG
                elif not own_on_file:
                    mg_white += ROOK_SEMI_OPEN_MG
                    eg_white += ROOK_SEMI_OPEN_EG

            if p_type in (chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
                attacks = board.attacks(sq)
                mob = len(attacks & ~board.occupied_co[chess.WHITE] & ~black_pawn_attacks)
                mg_white += MOBILITY_MG[p_type] * mob
                eg_white += MOBILITY_EG[p_type] * mob

        else:
            flipped_sq = FLIP_SQUARE[sq]
            mg_black += MG_VALUES[p_type] + PST_MG[p_type][flipped_sq]
            eg_black += EG_VALUES[p_type] + PST_EG[p_type][flipped_sq]

            if p_type == chess.PAWN:
                file = chess.square_file(sq)
                rank = chess.square_rank(sq)

                if len(black_pawns & chess.BB_FILES[file]) > 1:
                    mg_black -= 15
                    eg_black -= 20
                adj_files = 0
                if file > 0: adj_files |= chess.BB_FILES[file - 1]
                if file < 7: adj_files |= chess.BB_FILES[file + 1]
                if not (black_pawns & adj_files):
                    mg_black -= 12
                    eg_black -= 16

                if _is_passed_pawn(file, rank, chess.BLACK, white_pawn_list):
                    mg_black += PASSED_PAWN_MG[7 - rank]
                    eg_black += PASSED_PAWN_EG[7 - rank]

            elif p_type == chess.ROOK:
                file = chess.square_file(sq)
                own_on_file = black_pawns & chess.BB_FILES[file]
                enemy_on_file = white_pawns & chess.BB_FILES[file]
                if not own_on_file and not enemy_on_file:
                    mg_black += ROOK_OPEN_FILE_MG
                    eg_black += ROOK_OPEN_FILE_EG
                elif not own_on_file:
                    mg_black += ROOK_SEMI_OPEN_MG
                    eg_black += ROOK_SEMI_OPEN_EG

            if p_type in (chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN):
                attacks = board.attacks(sq)
                mob = len(attacks & ~board.occupied_co[chess.BLACK] & ~white_pawn_attacks)
                mg_black += MOBILITY_MG[p_type] * mob
                eg_black += MOBILITY_EG[p_type] * mob

    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        mg_white += 30
        eg_white += 40
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        mg_black += 30
        eg_black += 40

    
    
    if black_has_queen and white_king_sq is not None:
        kf = chess.square_file(white_king_sq)
        for f in range(max(0, kf - 1), min(7, kf + 1) + 1):
            if not (white_pawns & chess.BB_FILES[f]):
                mg_white -= KING_OPEN_FILE_PENALTY_MG
        mg_white -= _king_shield_penalty(white_king_sq, white_pawns, chess.WHITE) * KING_SHIELD_PENALTY_MG

    if white_has_queen and black_king_sq is not None:
        kf = chess.square_file(black_king_sq)
        for f in range(max(0, kf - 1), min(7, kf + 1) + 1):
            if not (black_pawns & chess.BB_FILES[f]):
                mg_black -= KING_OPEN_FILE_PENALTY_MG
        mg_black -= _king_shield_penalty(black_king_sq, black_pawns, chess.BLACK) * KING_SHIELD_PENALTY_MG

    phase = min(game_phase, MAX_PHASE)
    mg_score = mg_white - mg_black
    eg_score = eg_white - eg_black

    final_eval = ((mg_score * phase) + (eg_score * (MAX_PHASE - phase))) // MAX_PHASE

    result = final_eval if board.turn == chess.WHITE else -final_eval
    return result + TEMPO_BONUS


INFINITE_VAL = 1000000
MATE_THRESHOLD = 90000
MATE_SCORE_VAL = 99999


REVERSE_FUTILITY_MAX_DEPTH = 6
REVERSE_FUTILITY_MARGIN = 120
FUTILITY_MAX_DEPTH = 2
FUTILITY_MARGIN = {1: 150, 2: 300}
DELTA_MARGIN = 200
QUEEN_VALUE_MG = MG_VALUES[chess.QUEEN]
MAX_CHECK_EXTENSION_PLY = 40

LMP_MAX_DEPTH = 3
LMP_THRESHOLD = {1: 5, 2: 9, 3: 14}


class TranspositionTable:

    def __init__(self, max_size_mb=128):
        self.table = {}
        self.max_entries = (max_size_mb * 1024 * 1024) // 64

    def get(self, key):
        return self.table.get(key, None)

    def store(self, key, depth, score, flag, move, ply):
        if len(self.table) >= self.max_entries:
            self.table.clear()

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
        self.history_scores = {}
        self.nodes_searched = 0
        self.stop_search = False
        self.start_time = 0.0
        self.time_limit = 10.0

        self.history_scores[chess.WHITE] = [[0] * 64 for _ in range(64)]
        self.history_scores[chess.BLACK] = [[0] * 64 for _ in range(64)]

    def clear_heuristics(self):
        self.killer_moves = [[None] * 2 for _ in range(128)]
        for color in (chess.WHITE, chess.BLACK):
            self.history_scores[color] = [[0] * 64 for _ in range(64)]

    def score_move(self, move, pv_move, ply):
        
        if move == pv_move:
            return 1000000

        if self.board.is_capture(move):
            attacker = self.board.piece_at(move.from_square)
            target = self.board.piece_at(move.to_square)

            if target is None and self.board.is_en_passant(move):
                target_val = MG_VALUES[chess.PAWN]
            else:
                target_val = MG_VALUES[target.piece_type] if target else 100
            attacker_val = MG_VALUES[attacker.piece_type] if attacker else 100
            return 900000 + (target_val * 10 - attacker_val)

        if move.promotion:
            return 800000 + MG_VALUES[move.promotion]

        if 0 <= ply < 128:
            if move == self.killer_moves[ply][0]:
                return 700000
            if move == self.killer_moves[ply][1]:
                return 650000

        color = self.board.turn
        h_score = self.history_scores[color][move.from_square][move.to_square]
        if h_score > 0:
            return min(600000, h_score)

        return 0

    def _see(self, move):
        
        try:
            board = self.board
            to_sq = move.to_square

            if board.is_en_passant(move):
                captured_value = MG_VALUES[chess.PAWN]
            else:
                captured_piece = board.piece_at(to_sq)
                if captured_piece is None:
                    return 0
                captured_value = MG_VALUES[captured_piece.piece_type]

            moving_piece = board.piece_at(move.from_square)
            if moving_piece is None:
                return 0

            pushed = 0
            try:
                board.push(move)
                pushed += 1

                gains = [captured_value]
                attacker_value = MG_VALUES[moving_piece.piece_type]
                side = board.turn

                for _ in range(31):
                    attackers = board.attackers(side, to_sq)
                    if not attackers:
                        break

                    least_sq = None
                    least_val = None
                    for sq in attackers:
                        p = board.piece_at(sq)
                        if p is None:
                            continue
                        v = MG_VALUES[p.piece_type]
                        if least_val is None or v < least_val:
                            least_val = v
                            least_sq = sq

                    if least_sq is None:
                        break

                    recapture = chess.Move(least_sq, to_sq)
                    moving_p = board.piece_at(least_sq)
                    if (moving_p and moving_p.piece_type == chess.PAWN
                            and chess.square_rank(to_sq) in (0, 7)):
                        recapture = chess.Move(least_sq, to_sq, promotion=chess.QUEEN)

                    gains.append(attacker_value - gains[-1])
                    attacker_value = least_val

                    board.push(recapture)
                    pushed += 1
                    side = board.turn

                for i in range(len(gains) - 1, 0, -1):
                    gains[i - 1] = -max(-gains[i - 1], gains[i])

                return gains[0]
            finally:
                for _ in range(pushed):
                    board.pop()
        except Exception:
            return 0

    def quiescence_search(self, alpha, beta, ply):

        self.nodes_searched += 1

        if self.nodes_searched % 512 == 0 and time.time() - self.start_time >= self.time_limit:
            self.stop_search = True
            return alpha

        in_check = self.board.is_check()

        if in_check:
            
            
            moves = list(self.board.generate_legal_moves())
            if not moves:
                return -MATE_SCORE_VAL + ply
            moves.sort(key=lambda m: self.score_move(m, None, 0), reverse=True)

            for move in moves:
                self.board.push(move)
                score = -self.quiescence_search(-beta, -alpha, ply + 1)
                self.board.pop()

                if self.stop_search:
                    return alpha

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

            return alpha

        stand_pat = evaluate_board(self.board)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        candidates = [m for m in self.board.generate_legal_moves()
                      if self.board.is_capture(m) or m.promotion]

        scored_moves = []
        for m in candidates:
            if m.promotion:
                order_val = 800000 + MG_VALUES[m.promotion]
            else:
                attacker_piece = self.board.piece_at(m.from_square)
                attacker_val = MG_VALUES[attacker_piece.piece_type] if attacker_piece else 0

                if self.board.is_en_passant(m):
                    target_val = MG_VALUES[chess.PAWN]
                else:
                    target_piece = self.board.piece_at(m.to_square)
                    target_val = MG_VALUES[target_piece.piece_type] if target_piece else 0

                if attacker_val <= target_val:
                    
                    order_val = target_val - attacker_val
                else:
                    order_val = self._see(m)
            scored_moves.append((order_val, m))
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        for order_val, move in scored_moves:

            
            
            if not move.promotion and order_val < 0:
                continue

            if self.board.is_en_passant(move):
                cap_val = MG_VALUES[chess.PAWN]
            else:
                captured = self.board.piece_at(move.to_square)
                cap_val = MG_VALUES[captured.piece_type] if captured else 0

            if move.promotion:
                cap_val += MG_VALUES[move.promotion] - MG_VALUES[chess.PAWN]

            if stand_pat + cap_val + DELTA_MARGIN < alpha:
                continue

            self.board.push(move)
            score = -self.quiescence_search(-beta, -alpha, ply + 1)
            self.board.pop()

            if self.stop_search:
                return alpha

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def negamax(self, depth, alpha, beta, ply, allow_null=True):

        self.nodes_searched += 1

        if self.nodes_searched % 512 == 0 and time.time() - self.start_time >= self.time_limit:
            self.stop_search = True
            return alpha

        if self.board.is_checkmate():
            return -MATE_SCORE_VAL + ply
        if (
            self.board.is_stalemate()
            or self.board.is_insufficient_material()
            or self.board.is_repetition(3)
            or self.board.is_seventyfive_moves()
        ):
            return 0

        in_check = self.board.is_check()

        
        
        if in_check and ply < MAX_CHECK_EXTENSION_PLY:
            depth += 1

        if depth <= 0:
            return self.quiescence_search(alpha, beta, ply)

        zobrist_key = chess.polyglot.zobrist_hash(self.board)
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

        
        
        static_eval = None
        if not in_check and depth <= REVERSE_FUTILITY_MAX_DEPTH and abs(beta) < MATE_THRESHOLD:
            static_eval = evaluate_board(self.board)
            margin = REVERSE_FUTILITY_MARGIN * depth
            if static_eval - margin >= beta:
                return beta

        if allow_null and not in_check and depth >= 3:
            major_pieces = (
                self.board.knights | self.board.bishops | self.board.rooks | self.board.queens
            ) & self.board.occupied_co[self.board.turn]

            if major_pieces:
                R = 3 if depth >= 6 else 2
                self.board.push(chess.Move.null())
                null_score = -self.negamax(depth - 1 - R, -beta, -beta + 1, ply + 1, allow_null=False)
                self.board.pop()

                if self.stop_search:
                    return alpha
                if null_score >= beta:
                    return beta

        moves = list(self.board.generate_legal_moves())
        if not moves:
            if in_check:
                return -MATE_SCORE_VAL + ply
            return 0
        moves.sort(key=lambda m: self.score_move(m, pv_move, ply), reverse=True)

        can_use_futility = (
            static_eval is not None
            and depth <= FUTILITY_MAX_DEPTH
            and abs(alpha) < MATE_THRESHOLD
        )

        best_score = -INFINITE_VAL
        best_move = None
        alpha_original = alpha
        flag = 'UPPER'
        moves_searched = 0
        quiet_count = 0
        first_move = True

        for move in moves:
            is_capture = self.board.is_capture(move)
            is_promotion = bool(move.promotion)
            is_quiet = not is_capture and not is_promotion

            
            
            need_gives_check = (
                is_quiet and not first_move and not in_check
                and (depth <= LMP_MAX_DEPTH or can_use_futility)
                and abs(alpha) < MATE_THRESHOLD
            )
            gives_check_flag = self.board.gives_check(move) if need_gives_check else False

            
            
            if is_quiet and not first_move and not in_check:
                quiet_count += 1
                if (depth <= LMP_MAX_DEPTH
                        and quiet_count > LMP_THRESHOLD.get(depth, 999)
                        and abs(alpha) < MATE_THRESHOLD
                        and not gives_check_flag):
                    moves_searched += 1
                    continue

            
            
            if can_use_futility and not first_move and not is_capture and not is_promotion:
                if not gives_check_flag:
                    margin = FUTILITY_MARGIN[depth]
                    if static_eval + margin <= alpha:
                        moves_searched += 1
                        continue

            self.board.push(move)
            moves_searched += 1

            if first_move:
                score = -self.negamax(depth - 1, -beta, -alpha, ply + 1)
            else:
                if depth >= 3 and moves_searched > 4 and not in_check and not is_capture and not is_promotion:
                    reduction = 2 if moves_searched > 12 else 1
                    reduced_depth = max(1, depth - 1 - reduction)
                    score = -self.negamax(reduced_depth, -alpha - 1, -alpha, ply + 1)
                else:
                    score = -self.negamax(depth - 1, -alpha - 1, -alpha, ply + 1)

                if score > alpha and score < beta:
                    score = -self.negamax(depth - 1, -beta, -alpha, ply + 1)

            self.board.pop()
            first_move = False

            if self.stop_search:
                return alpha

            if score > best_score:
                best_score = score
                best_move = move

            if score > alpha:
                alpha = score
                flag = 'EXACT'

            if alpha >= beta:
                if not is_capture:
                    if 0 <= ply < 128:
                        self.killer_moves[ply][1] = self.killer_moves[ply][0]
                        self.killer_moves[ply][0] = move

                    color = self.board.turn
                    self.history_scores[color][move.from_square][move.to_square] += depth * depth

                self.tt.store(zobrist_key, depth, beta, 'LOWER', move, ply)
                return beta

        if best_score <= alpha_original:
            flag = "UPPER"
        elif best_score >= beta:
            flag = "LOWER"
        else:
            flag = "EXACT"

        self.tt.store(
             zobrist_key,
             depth,
             best_score,
             flag,
             best_move,
             ply
        )
        return best_score

    def search(self, depth_limit, time_limit):

        self.start_time = time.time()
        self.time_limit = max(0.02, time_limit)
        self.stop_search = False
        self.nodes_searched = 0

        legal_moves = list(self.board.generate_legal_moves())
        if not legal_moves:
            return None
        if len(legal_moves) == 1:
            return legal_moves[0]

        best_move = legal_moves[0]
        last_completed_score = 0
        last_iter_duration = 0.0

        for current_depth in range(1, depth_limit + 1):
            try:
                elapsed_so_far = time.time() - self.start_time
                if elapsed_so_far >= self.time_limit:
                    break

                
                
                
                if current_depth > 5 and last_iter_duration > 0:
                    projected = elapsed_so_far + last_iter_duration * 2.3
                    if projected > self.time_limit:
                        break

                iter_start = time.time()

                if current_depth >= 4:
                    window = 25
                    alpha = last_completed_score - window
                    beta = last_completed_score + window
                else:
                    window = INFINITE_VAL
                    alpha = -INFINITE_VAL
                    beta = INFINITE_VAL

                iter_best_move = None
                best_score = last_completed_score
                fail_lows = 0
                fail_highs = 0

                while True:
                    alpha_original = alpha
                    beta_original = beta

                    z_key = chess.polyglot.zobrist_hash(self.board)
                    tt_entry = self.tt.get(z_key)
                    pv_move = tt_entry['move'] if tt_entry else None

                    moves = list(self.board.generate_legal_moves())
                    moves.sort(key=lambda m: self.score_move(m, pv_move, 0), reverse=True)

                    best_score = -INFINITE_VAL
                    iter_best_move = None
                    search_alpha = alpha_original
                    search_beta = beta_original

                    for move in moves:
                        self.board.push(move)
                        score = -self.negamax(current_depth - 1, -search_beta, -search_alpha, 1)
                        self.board.pop()

                        if self.stop_search:
                            break

                        if score > best_score:
                            best_score = score
                            iter_best_move = move

                        search_alpha = max(search_alpha, score)
                        if search_alpha >= search_beta:
                            break

                    if self.stop_search:
                        break

                    
                    
                    if best_score <= alpha_original and alpha_original > -INFINITE_VAL:
                        fail_lows += 1
                        window = window * 3 if window < INFINITE_VAL else INFINITE_VAL
                        if fail_lows >= 3 or window >= INFINITE_VAL:
                            alpha = -INFINITE_VAL
                        else:
                            alpha = max(-INFINITE_VAL, last_completed_score - window)
                        beta = beta_original
                        continue

                    elif best_score >= beta_original and beta_original < INFINITE_VAL:
                        fail_highs += 1
                        window = window * 3 if window < INFINITE_VAL else INFINITE_VAL
                        if fail_highs >= 3 or window >= INFINITE_VAL:
                            beta = INFINITE_VAL
                        else:
                            beta = min(INFINITE_VAL, last_completed_score + window)
                        alpha = alpha_original
                        continue
                    else:
                        last_completed_score = best_score
                        break

                last_iter_duration = time.time() - iter_start

                if not self.stop_search and iter_best_move:
                    best_move = iter_best_move
                    score_str = f"cp {best_score}" if abs(best_score) < MATE_THRESHOLD else f"mate {int((MATE_SCORE_VAL - abs(best_score)) / 2) + 1}"
                    print(f"info depth {current_depth} score {score_str} nodes {self.nodes_searched} time {int((time.time() - self.start_time) * 1000)} pv {best_move.uci()}", flush=True)

                if self.stop_search:
                    break

                if time.time() - self.start_time >= self.time_limit:
                    break

            except Exception as e:
                sys.stderr.write(f"Iteration exception at depth {current_depth}: {str(e)}\n")
                sys.stderr.flush()
                break

        return best_move


# UCI

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
                print("id name Ruthless v2.2", flush=True)
                print("id author Dr.Flatpawn & Claude", flush=True)
                print("uciok", flush=True)

            elif cmd == "isready":
                print("readyok", flush=True)

            elif cmd == "ucinewgame":
                engine.board = chess.Board()
                engine.tt.table.clear()
                engine.clear_heuristics()

            elif cmd == "position":
                moves_idx = None
                if len(tokens) > 1 and tokens[1] == "startpos":
                    engine.board = chess.Board()
                    moves_idx = 2
                elif len(tokens) > 1 and tokens[1] == "fen":
                    fen_parts = []
                    idx = 2
                    while idx < len(tokens) and tokens[idx] != "moves":
                        fen_parts.append(tokens[idx])
                        idx += 1
                    try:
                        engine.board = chess.Board(" ".join(fen_parts))
                    except Exception as e:
                        sys.stderr.write(f"Bad FEN: {str(e)}\n")
                        sys.stderr.flush()
                    moves_idx = idx

                if moves_idx is not None and moves_idx < len(tokens) and tokens[moves_idx] == "moves":
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
                movestogo = None
                depth_limit = 20

                for i in range(1, len(tokens), 2):
                    if i + 1 >= len(tokens):
                        break
                    param = tokens[i]
                    val = tokens[i + 1]

                    if param == "wtime": wtime = int(val)
                    elif param == "btime": btime = int(val)
                    elif param == "winc": winc = int(val)
                    elif param == "binc": binc = int(val)
                    elif param == "movetime": movetime = int(val)
                    elif param == "movestogo": movestogo = int(val)
                    elif param == "depth": depth_limit = int(val)

                search_time = 3.0
                if movetime is not None:
                    search_time = (movetime / 1000.0) * 0.95
                else:
                    my_time = wtime if engine.board.turn == chess.WHITE else btime
                    my_inc = winc if engine.board.turn == chess.WHITE else binc

                    if my_time is not None:
                        my_inc = my_inc or 0
                        overhead = 30  
                        usable_time = max(0, my_time - overhead)

                        if movestogo:
                            base_allocation = usable_time / max(1, movestogo)
                        else:
                            moves_played = engine.board.fullmove_number
                            estimated_moves_left = max(15, 50 - moves_played)
                            base_allocation = usable_time / estimated_moves_left

                        inc_allocation = my_inc * 0.8
                        search_time = (base_allocation + inc_allocation) / 1000.0

                        search_time = max(0.015, min(search_time, (usable_time * 0.5) / 1000.0))

                        if my_time < 1000:
                            search_time = min(search_time, max(0.01, (my_time * 0.1) / 1000.0))

                best_move = None
                try:
                    best_move = engine.search(depth_limit=depth_limit, time_limit=search_time)
                except Exception as e:
                    sys.stderr.write(f"Search exception: {str(e)}\n")
                    sys.stderr.flush()
                    best_move = None

                if best_move is None:
                    try:
                        legal = list(engine.board.legal_moves)
                    except Exception:
                        legal = []
                    best_move = legal[0] if legal else None

                if best_move is not None:
                    print(f"bestmove {best_move.uci()}", flush=True)
                else:
                    print("bestmove 0000", flush=True)

            elif cmd == "quit":
                break

        except Exception as e:
            sys.stderr.write(f"Exception in UCI Loop: {str(e)}\n")
            sys.stderr.flush()
            
            
            try:
                if 'cmd' in dir() and cmd == "go":
                    legal = list(engine.board.legal_moves)
                    if legal:
                        print(f"bestmove {legal[0].uci()}", flush=True)
                    else:
                        print("bestmove 0000", flush=True)
            except Exception:
                pass

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