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
