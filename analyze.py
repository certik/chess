from chess.pgn import PGNReader
from chess.board import Board

p = PGNReader(open("op.pgn").read())
b = Board()
b.moves_from_list(p.moves_as_list())
print b
