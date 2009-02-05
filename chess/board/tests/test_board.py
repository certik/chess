from board import Board

def test_setup1():
    b = Board()
    assert b.to_string() ==  \
        "RNBQKBNRPPPPPPPP                                pppppppprnbqkbnr"

def test_setup2():
    b = Board()
    b.move_algebraic("e4")
    assert b.to_string() ==  \
        "RNBQKBNRPPPPPPPP                    p           pppp ppprnbqkbnr"
