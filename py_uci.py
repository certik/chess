import sys
import pexpect

class UCIEngine(object):

    def __init__(self, executable="stockfish", debug=True):
        self._p = pexpect.spawn("stockfish")
        if debug:
            self._p.logfile = sys.stdout
        self._p.sendline("uci")
        self._p.sendline("setoption name Hash value 1024")
        self._p.expect("uciok")
        self._p.sendline("ucinewgame")
        self._p.sendline("isready")
        self._p.expect("readyok")

    def new_game(self):
        self._p.sendline("position startpos")

    def make_move(self, move):
        """
        Make the move 'move' on the internal chessboard.

        The move has to be a valid move, otherwise the engine can segfault
        later on.
        """
        self._p.sendline("position moves %s" % move)

    def make_moves(self, moves):
        """
        Make the move 'moves' on the internal chessboard.

        'moves' is a list of moves.

        The move has to be a valid move, otherwise the engine can segfault
        later on.
        """
        self._p.sendline("position moves %s" % " ".join(moves))

    def find_best_move(self, movetime=2):
        if movetime is None:
            self._p.sendline("go infinite")
        else:
            self._p.sendline("go movetime %d" % movetime)
        self._p.expect("bestmove (\S+) ponder (\S+)", timeout=None)
        best_move, ponder = self._p.match.groups()
        return best_move, ponder

def get_move_from_user(default="e2e4"):
    print "Your move (%s):" % default
    move = raw_input()
    if move == "":
        move = default
    print "Using the move:", move
    return move

if __name__ == "__main__":
    e = UCIEngine()
    e.new_game()
    ponder = "e2e4"
    i = 0
    while 1:
        i += 1
        if i < 30:
            move = ponder
        else:
            move = get_move_from_user(ponder)
        e.make_move(move)
        best_move, ponder = e.find_best_move()
        e.make_move(best_move)
        print "computer:", best_move
