import sys
import pexpect

class UCIEngine(object):

    def __init__(self, executable="stockfish", debug=True, multi_pv=1):
        self._p = pexpect.spawn("stockfish", encoding="us-ascii")
        if debug:
            self._p.logfile = sys.stdout
        self._p.sendline("uci")
        # Set the memory usage (roughly 3GB)
        self._p.sendline("setoption name Hash value 3072")
        self._p.sendline("setoption name MultiPV value %d" % multi_pv)
        self._p.expect("uciok")

    def new_game(self):
        self._p.sendline("ucinewgame")
        self._p.sendline("isready")
        self._p.expect("readyok")

    def set_position(self, initial_position=None, moves=None):
        """
        Sets the position on the internal chessboard.

        initial_position ... If None, start position is used, otherwise specify
                             a position in a "fen" format.
        moves ... List of moves to make, in algebraic notation from
                  "initial_position". Moves have to valid, otherwise the engine
                  can segfault later on.
        """
        if moves:
            assert len(moves) >= 1
            s_moves = "moves " + " ".join(moves)
        else:
            s_moves = ""
        if initial_position:
            self._p.sendline("position fen %s %s" % (initial_position,
                s_moves))
        else:
            self._p.sendline("position startpos %s" % s_moves)

    def find_best_move(self, movetime=2):
        if movetime is None:
            self._p.sendline("go infinite")
        else:
            self._p.sendline("go movetime %d" % movetime)
        self._p.expect(r"bestmove (\S+) ponder (\S+)", timeout=None)
        best_move, ponder = self._p.match.groups()
        return best_move, ponder

def get_move_from_user(default="e2e4"):
    print("Your move (%s):" % default)
    move = input()
    if move == "":
        move = default
    print("Using the move:", move)
    return move

if __name__ == "__main__":
    e = UCIEngine()
    e.new_game()
    ponder = "e2e4"
    i = 0
    moves = []
    while 1:
        i += 1
        if i < 30:
            move = ponder
        else:
            move = get_move_from_user(ponder)
        print("you:", move)
        moves.append(move)
        e.set_position(moves=moves)
        best_move, ponder = e.find_best_move()
        moves.append(best_move)
        print("computer:", best_move)
