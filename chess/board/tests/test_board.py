from board import Board

def test_setup1():
    b = Board()
    assert b.to_string() ==  \
        "RNBQKBNRPPPPPPPP                                pppppppprnbqkbnr"

def test_moves1():
    b = Board()
    b.move_algebraic("e4")
    assert b.to_string() ==  \
        "RNBQKBNRPPPPPPPP                    p           pppp ppprnbqkbnr"

def test_moves2():
    b = Board()
    b.move_algebraic("e4")
    b.move_algebraic("e5")
    b.move_algebraic("Nf3")
    b.move_algebraic("Nc6")
    b.move_algebraic("Bb5")
    b.move_algebraic("a6")
    b.move_algebraic("Bxc6")
    assert b.to_string() ==  \
        "R BQKBNR PPP PPPP b         P       p        n  pppp ppprnbqk  r"

def test_moves3():
    b = Board()
    b.move_algebraic("e4")
    b.move_algebraic("e5")
    b.move_algebraic("Nf3")
    b.move_algebraic("Nc6")
    b.move_algebraic("Bb5")
    b.move_algebraic("a6")
    b.move_algebraic("Bxc6")
    b.move_algebraic("dxc6")
    assert b.to_string() ==  \
        "R BQKBNR PP  PPPP P         P       p        n  pppp ppprnbqk  r"

def test_moves4():
    b = Board()
    b.move_algebraic("e4")
    b.move_algebraic("e5")
    b.move_algebraic("Nf3")
    b.move_algebraic("Nc6")
    b.move_algebraic("Bb5")
    b.move_algebraic("a6")
    b.move_algebraic("Bxc6")
    b.move_algebraic("dxc6")
    b.move_algebraic("d3")
    b.move_algebraic("Bb4+")
    b.move_algebraic("Nc3")
    b.move_algebraic("Nf6")
    b.move_algebraic("O-O")
    b.move_algebraic("Bxc3")
    b.move_algebraic("Re1")
    assert b.to_string() ==  \
        "R BQK  R PP  PPPP P  N      P       p     Bp n  ppp  pppr bqr k "

def test_moves5():
    moves = ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'a6', 'Ba4', 'Nf6', 'O-O', 'Be7', 'Re1', 'b5', 'Bb3', 'd6', 'c3', 'O-O', 'h3', 'Nb8', 'd4', 'Nbd7', 'c4', 'c6', 'cxb5', 'axb5', 'Nc3', 'Bb7', 'Bg5', 'b4', 'Nb1', 'h6', 'Bh4', 'c5', 'dxe5', 'Nxe4', 'Bxe7', 'Qxe7', 'exd6', 'Qf6', 'Nbd2', 'Nxd6', 'Nc4', 'Nxc4', 'Bxc4', 'Nb6', 'Ne5', 'Rae8', 'Bxf7+', 'Rxf7', 'Nxf7', 'Rxe1+', 'Qxe1', 'Kxf7', 'Qe3', 'Qg5', 'Qxg5', 'hxg5', 'b3', 'Ke6', 'a3', 'Kd6', 'axb4', 'cxb4', 'Ra5', 'Nd5', 'f3', 'Bc8', 'Kf2', 'Bf5', 'Ra7', 'g6', 'Ra6+', 'Kc5', 'Ke1', 'Nf4', 'g3', 'Nxh3', 'Kd2', 'Kb5', 'Rd6', 'Kc5', 'Ra6', 'Nf2', 'g4', 'Bd3', 'Re6']
    b = Board()
    for move in moves:
        b.move_algebraic(move)
    assert b.to_string() == \
        "                    r P   K   P  P    p  p B p     k N          "

def test_moves6():
    moves = ['d4', 'Nf6', 'c4', 'c5', 'd5', 'b5', 'Nf3', 'b4', 'Nbd2', 'g6', 'b3', 'Bg7', 'Bb2', 'O-O', 'e4', 'd6', 'Qc2', 'e5', 'dxe6', 'Bxe6', 'g3', 'Nc6', 'Bg2', 'Bg4', 'O-O', 'Nd7', 'h3', 'Bxf3', 'Nxf3', 'Bxb2', 'Qxb2', 'Nde5', 'Ne1', 'Nd4', 'f4', 'Nec6', 'Nd3', 'a5', 'Rad1', 'a4', 'Kh2', 'axb3', 'axb3', 'Ra3', 'Nc1', 'Qf6', 'Rf2', 'Rfa8', 'Re1', 'Qe7', 'Re3', 'Ra1', 'e5', 'dxe5', 'Nd3', 'R8a2', 'Qxa2', 'Rxa2', 'Rxa2', 'Nf5', 'Re1', 'Qd6', 'Bd5', 'exf4', 'Nxf4', 'h5', 'h4', 'Nce7', 'Rd2', 'Kg7', 'Rd3', 'Nxg3', 'Rxe7', 'Nf1+', 'Kg2', 'Qxe7', 'Kxf1', 'Qxh4', 'Rf3', 'Qh1+', 'Ke2', 'Qb1', 'Nxh5+', 'gxh5', 'Rxf7+', 'Kh6', 'Rf3', 'Qg1', 'Rf6+', 'Kg5', 'Rf2', 'Qb1', 'Rf3', 'Qc2+', 'Ke1', 'Kg4', 'Re3', 'h4', 'Bb7', 'Qh2', 'Kf1', 'Qd2', 'Bc8+', 'Kf4', 'Rh3', 'Qd8', 'Bb7', 'Qd1+', 'Kf2', 'Qc2+', 'Kf1', 'Qd1+', 'Kf2', 'Qd2+', 'Kf1', 'Ke5', 'Bg2', 'Qg5', 'Kf2', 'Kd4', 'Rf3', 'Qc1', 'Bh3', 'Qd2+', 'Kf1', 'Qd1+', 'Kf2', 'Qh1', 'Bg2', 'Qc1', 'Bh3', 'Qb2+', 'Kf1', 'Qc3', 'Kf2', 'Qd2+', 'Kf1', 'Ke4', 'Bg2', 'Ke5', 'Bh3', 'Kd4', 'Bg2', 'Qa2', 'Bh3', 'Qh2', 'Bg2', 'Qe5', 'Kf2', 'Qe4', 'Bh3', 'Qc2+', 'Kf1', 'Qd2', 'Bg2', 'Qc1+', 'Kf2', 'Qb2+', 'Kf1', 'Qa1+', 'Kf2', 'Ke4', 'Rh3+', 'Kf5', 'Rf3+', 'Kg5', 'Bh3', 'Qb2+', 'Kf1', 'Qc2', 'Ke1', 'Qe4+', 'Kf2', 'Qb1', 'Kg2', 'Qe1', 'Rf5+', 'Kg6', 'Rf3', 'Kg7', 'Rf2', 'Qd1', 'Rf3', 'Qd2+', 'Kf1', 'Kg6', 'Bg2', 'Qd1+', 'Kf2', 'Qd4+', 'Kf1', 'Qg4', 'Kf2', 'Kg5', 'Bh3', 'Qe4', 'Kg2', 'Qe2+', 'Rf2']
    b = Board()
    for move in moves:
        b.move_algebraic(move)
    assert b.to_string() == \
        "                          P   K  Pp    P p     b    Qrk         "

def test_moves7():
    moves = ['d4', 'Nf6', 'c4', 'c5', 'd5', 'b5', 'cxb5', 'a6', 'e3', 'Bb7', 'Nc3', 'axb5', 'Bxb5', 'Qa5', 'Bd2', 'Qb6', 'Nf3', 'Nxd5', 'Nxd5', 'Bxd5', 'a4', 'e6', 'Bc3', 'Be7', 'O-O', 'O-O', 'Ne5', 'd6', 'Nc4', 'Bxc4', 'Qg4', 'g6', 'Qxc4', 'Nc6', 'e4', 'Nd4', 'Bxd4', 'cxd4', 'Rfc1', 'Bg5', 'Rc2', 'Kg7', 'b4', 'Rfc8', 'Qxc8', 'Rxc8', 'Rxc8', 'd3', 'Bxd3', 'Qd4', 'Rd1', 'Qxb4', 'Bc2', 'Bf6', 'h3', 'Bd4', 'Rf1', 'Bc5', 'Ra8', 'h5', 'a5', 'Qb7', 'Re8', 'Qa6', 'Bd1', 'Qxa5', 'Bf3', 'h4', 'Re7', 'Qb4', 'Rc7', 'Qb6', 'Rc8', 'Qb7', 'Re8', 'Qb2', 'Bd1', 'Qd2', 'Bf3', 'Qd4', 'Ra8', 'Kf6', 'Ra2', 'Qe5', 'Rc1', 'Qf4', 'Rc4', 'Ke5', 'Re2', 'Qg5', 'Kf1', 'Qd8', 'Rcc2', 'Qa5', 'Ra2', 'Qc3', 'Rac2', 'Qd3', 'Kg1', 'Qd1+', 'Kh2', 'Qa1', 'Ra2', 'Qc3', 'Rec2', 'Qd4', 'Rd2', 'Qc3', 'Rdc2', 'Qe1', 'Re2', 'Qb1', 'Rac2', 'Bd4', 'Rcd2', 'Qb4', 'Rc2', 'Kf6', 'g3', 'hxg3+', 'Kxg3', 'Be5+', 'Kg2', 'Qb8', 'h4', 'Qh8', 'Kh3', 'Qh6', 'Re1', 'Qf4', 'Kg2', 'Qh2+', 'Kf1', 'Qxh4', 'Rd1', 'Qh8', 'Ke2', 'Qb8', 'Rcd2', 'Qb5+', 'Rd3', 'Qc4', 'Rg1', 'Bf4', 'Rgd1', 'Ke5', 'Ke1', 'Kf6', 'Rd4', 'Qc3+', 'Ke2', 'Qc2+', 'Kf1', 'Kg5', 'Be2', 'f5', 'f3', 'Qc3', 'R1d3', 'Qc7', 'Bd1', 'Qh7', 'exf5', 'Qh1+', 'Kf2', 'Qh2+', 'Kf1', 'gxf5', 'Bb3', 'Bg3', 'f4+', 'Kf6', 'Rd2', 'Qh1+', 'Ke2', 'Qg2+', 'Kd3', 'Qf3+', 'Kc2', 'Bxf4', 'Rd1', 'Qe2+', 'Kb1', 'Be5', 'R4d2', 'Qe4+', 'Rd3', 'd5', 'Bc2', 'Qb4+', 'Rb3', 'Qa5', 'Kc1', 'Qa1+', 'Kd2', 'Qd4+', 'Kc1', 'Qc5', 'Rf1', 'Bd4', 'Kd2', 'Qc4', 'Rff3', 'Be5', 'Kd1', 'Bd6', 'Rbc3', 'Qg4', 'Ke2', 'f4', 'Kf1', 'Bc5', 'Ke2', 'Bd6', 'Bb3', 'Be5', 'Rcd3', 'Bd6', 'Kf1', 'Bc5', 'Ke1', 'Ke5', 'Kd2', 'Be3+', 'Rdxe3+', 'fxe3+', 'Rxe3+', 'Kd6', 'Bc2', 'e5', 'Ke1', 'e4', 'Kd2', 'Ke5', 'Re2', 'Qf3', 'Bd1', 'd4', 'Kc1', 'Qc3+', 'Kb1', 'd3', 'Rh2', 'Kd4', 'Ka2', 'Qa5+', 'Kb2', 'Qc3+', 'Ka2', 'Qc1', 'Rh8', 'Qxd1', 'Ka3', 'Qb1', 'Rd8+', 'Ke3'] 
    b = Board()
    for move in moves:
        b.move_algebraic(move)
    assert b.to_string() == \
        "   r                                P   k  PK            Q      "
