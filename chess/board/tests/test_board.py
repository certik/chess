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
