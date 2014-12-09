import sys

files, ranks = None, None
K, Q, R, B, N = range(5)

def memo(f):
    cache = {}
    def wrapper(*args):
        r = cache.get(args)
        if r is None:
            r = f(*args)
            cache[args] = r
        return r
    return wrapper

def sq_2_idx(f, r):
    return f * ranks + r

def idx_2_sq(idx):
    return divmod(idx, ranks)

def king_attacks((f, r), (_f, _r)):
    return abs(f - _f) <= 1 and abs(r - _r) <= 1

def queen_attacks(sq, _sq):
    return rook_attacks(sq, _sq) or bishop_attacks(sq, _sq)

def rook_attacks((f, r), (_f, _r)):
    return f == _f or r == _r

def bishop_attacks((f, r), (_f, _r)):
    return abs(f - _f) == abs(r - _r)

def knight_attacks((f, r), (_f, _r)):
    df, dr = abs(f - _f), abs(r - _r)
    return df + dr == 0 or df + dr == 3 and df > 0 and dr > 0

attacks = (king_attacks, queen_attacks, rook_attacks, bishop_attacks, knight_attacks)

@memo
def piece_attacks(piece, from_idx, target_idx):
    return attacks[piece](idx_2_sq(from_idx), idx_2_sq(target_idx))

def sort_pieces(k, q, r, b, n): 
    return [p for i, n in [(Q, q), (R, r), (B, b), (K, k), (N, n)] for p in [i] * n]

def drop_threatened(safe_squares, piece, idx):
    return filter(lambda i: not piece_attacks(piece, idx, i), safe_squares)

def new_piece_attacks(pieces_on_board, piece, idx):
    return next((True for i, _ in pieces_on_board if piece_attacks(piece, idx, i)), False)

def solve(fs, rs, k = 0, q = 0, r = 0, b = 0, n = 0):
    global files, ranks
    files, ranks = fs, rs
    stack = [(range(files * ranks), sort_pieces(k, q, r, b, n), [], 0)]
    solutions = []

    while stack:
        safe_squares, piece_seq, pieces_on_board, idx = stack.pop()

        if not piece_seq:
            solutions.append(pieces_on_board)

        elif len(safe_squares) < len(piece_seq):
            pass
        
        else:
            piece, rem_pieces = piece_seq[0], piece_seq[1:]
            for i in filter(lambda x: x >= idx, safe_squares):
                if not new_piece_attacks(pieces_on_board, piece, i):
                    safe_sqs = drop_threatened(safe_squares, piece, i)
                    j = i + 1 if rem_pieces and piece == rem_pieces[0] else 0
                    stack.append((safe_sqs, rem_pieces, pieces_on_board + [(i, piece)], j))

    return solutions

def print_solution(pieces_on_board):
    board = ["."] * files * ranks
    pcs = ["K", "Q", "R", "B", "N"]
    for i, p in pieces_on_board:
        board[i] = pcs[p]
    for r in xrange(ranks):
        for f in xrange(files):
            print board[sq_2_idx(f, r)],
        print 
    print

def test():
    assert len(solve(2, 2, k = 1, b = 1)) == 0
    assert len(solve(4, 4, r = 2, n = 4)) == 8
    assert len(solve(4, 4, b = 6)) == 16
    assert len(solve(8, 8, q = 8)) == 92

def main():
    solutions = solve(*map(int, sys.stdin.readline().split()))
    print len(solutions), "solutions\n"
    if solutions:
        print_solution(solutions[0])

if __name__ == "__main__":
    main()