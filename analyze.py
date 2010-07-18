from chess.pgn import PGNReader
from chess.board import Board
from py_uci import UCIEngine

p = PGNReader(open("op.pgn").read())
b = Board()
b.moves_from_list(p.moves_as_list())
e = UCIEngine()
e.new_game()
e.make_moves(b.get_moves())
best_move, ponder = e.find_best_move(None)
print "computer:", best_move
