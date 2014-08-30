import sys

files, ranks = None, None

def inside(f, r):
    return 0 <= f < files and 0 <= r < ranks

def sq_2_idx(sq):
    return sq[0] * files + sq[1]

def idx_2_sq(idx):
    return divmod(idx, files)

def king_moves(f, r):
    return [(x, y) for x in (f - 1, f, f + 1) for y in (r - 1, r, r + 1) if inside(x, y)]

def queen_moves(f, r):
    return rook_moves(f, r) + bishop_moves(f, r)

def rook_moves(f, r):
    return [(x, r) for x in xrange(files)] + [(f, y) for y in xrange(ranks)]

def bishop_moves(f, r):
    a1, b1 = min(f, r), min(files - f, ranks - r)
    a2, b2 = min(f, ranks - r - 1), min(files - f, r + 1)
    return zip(xrange(f - a1, f + b1), xrange(r - a1, r + b1)) + \
           zip(xrange(f - a2, f + b2), xrange(r + a2, r - b2, -1))

def knight_moves(f, r):
    return [(x, y) for x in (f - 2, f + 2) for y in (r - 1, r + 1) if inside(x, y)] + \
           [(x, y) for x in (f - 1, f + 1) for y in (r - 2, r + 2) if inside(x, y)] + [(f, r)]

def piece_moves(piece):
    return (king_moves, queen_moves, rook_moves, bishop_moves, knight_moves)[piece]

def next_pieces(piece_set):
    return [i for i in xrange(len(piece_set)) if piece_set[i] > 0]

def next_idx(board_coverage, idx):
    try:
        i = idx + 1
        return i + board_coverage[i:].index(False)
    except:
        return None

def pop_piece(piece_set, piece):
    ps = piece_set[:]
    ps[piece] -= 1
    return ps

def cover_board(board_coverage, moves):
    bc = board_coverage[:]
    for idx in moves:
        bc[idx] = True
    return bc

def safe_squares(board_coverage):
    return board_coverage.count(False)

def captures(pieces_on_board, moves):
    for idx, _ in pieces_on_board:
        if idx in moves:
            return True
    return False

def solve(fs, rs, k = 0, q = 0, r = 0, b = 0, n = 0):
    global files, ranks
    files, ranks = fs, rs
    stack = [([False] * files * ranks, [k, q, r, b, n], [], 0)]
    solutions = []

    while len(stack):
        board_coverage, piece_set, pieces_on_board, idx = stack.pop()
        pieces_left = sum(piece_set)

        if not pieces_left:
            solutions.append(pieces_on_board)

        elif idx is None or safe_squares(board_coverage) < pieces_left:
            pass
        
        else:
            stack.append((board_coverage, piece_set, pieces_on_board, 
                next_idx(board_coverage, idx)))

            for piece in next_pieces(piece_set):
                moves = map(sq_2_idx, piece_moves(piece)(*idx_2_sq(idx)))
                if not captures(pieces_on_board, moves):
                    bc = cover_board(board_coverage, moves)
                    ps = pop_piece(piece_set, piece)
                    pb = pieces_on_board + [(idx, piece)]
                    i  = next_idx(bc, idx)
                    stack.append((bc, ps, pb, i))
    return solutions

def print_solution(solution):
    board = ["."] * files * ranks
    pcs = ["K", "Q", "R", "B", "N"]
    for i, p in solution:
        board[i] = pcs[p]
    for r in xrange(ranks):
        for f in xrange(files):
            print board[sq_2_idx((f, r))],
        print 
    print 

def test():
    assert len(solve(2, 2, k = 1, b = 1)) == 0
    assert len(solve(4, 4, r = 2, n = 4)) == 8
    assert len(solve(4, 4, b = 6)) == 16
    assert len(solve(8, 8, q = 8)) == 92

def main():
    print len(solve(*map(int, sys.stdin.readline().split())))

if __name__ == "__main__":
    main()
