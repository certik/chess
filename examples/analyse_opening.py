from py_uci import UCIEngine
from chess.board import Board

b = Board()
b.move_algebraic("e4")
b.move_algebraic("c5")
b.move_algebraic("Nf3")
b.move_algebraic("d6")
b.move_algebraic("d4")
b.move_algebraic("cxd4")
b.move_algebraic("Nxd4")
b.move_algebraic("Nf6")
b.move_algebraic("Nc3")
b.move_algebraic("a6")
b.move_algebraic("g4")

e = UCIEngine(multi_pv=10)
e.new_game()
e.set_position(moves=b.get_moves())
e.find_best_move(10000)
print b
