from py_uci import UCIEngine

fen = "3rk2r/pb2n1bp/q1pB1pp1/2P1P3/8/1NN2Q2/PP3RPP/3R2K1 b - - 0 1"

e = UCIEngine()
e.new_game()
e.set_position(initial_position=fen)
e.find_best_move()
