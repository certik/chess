import sys
sys.path.append("..")
from py_uci import UCIEngine
from chess.board import Board

b = Board()
b.move_algebraic("e4")
b.move_algebraic("e5")
b.move_algebraic("Nf3")
b.move_algebraic("Nc6")
b.move_algebraic("Bc4")
b.move_algebraic("h6")
b.move_algebraic("O-O")
b.move_algebraic("Bc5")
b.move_algebraic("c3")
b.move_algebraic("Nf6")
b.move_algebraic("d4")
b.move_algebraic("exd4")
b.move_algebraic("cxd4")
b.move_algebraic("Bb6")
b.move_algebraic("e5")
b.move_algebraic("Nh7")
b.move_algebraic("d5")
b.move_algebraic("Ne7")
b.move_algebraic("d6")
b.move_algebraic("Nc6")

#b.move_algebraic("Bxf7")
#b.move_algebraic("Kxf7")
#b.move_algebraic("dxc7")
#b.move_algebraic("Qxc7")
#b.move_algebraic("Nc3")
#b.move_algebraic("Re8")
#b.move_algebraic("Nb5")
#b.move_algebraic("Qd8")
#b.move_algebraic("Nd6")
#b.move_algebraic("Kg8")


e = UCIEngine(multi_pv=10)
e.new_game()
e.set_position(moves=b.get_moves())
e.find_best_move(30000)
print b
