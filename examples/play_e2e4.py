from py_uci import UCIEngine
e = UCIEngine()
e.new_game()
e.set_position(moves=["e2e4"])
e.find_best_move()
