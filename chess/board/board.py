class InvalidMove(Exception):
    pass

class Board(object):

    def __init__(self):
        self._board = [None]*64
        self.setup()

    def setup(self):
        self[0, 0] = Rock(self)
        self[1, 0] = Knight(self)
        self[2, 0] = Bishop(self)
        self[3, 0] = Queen(self)
        self[4, 0] = King(self)
        self[5, 0] = Bishop(self)
        self[6, 0] = Knight(self)
        self[7, 0] = Rock(self)

        for i in range(8):
            self[i, 1] = Pawn(self)
            self[i, 6] = Pawn(self, black=True)

        self[0, 7] = Rock(self, black=True)
        self[1, 7] = Knight(self, black=True)
        self[2, 7] = Bishop(self, black=True)
        self[3, 7] = Queen(self, black=True)
        self[4, 7] = King(self, black=True)
        self[5, 7] = Bishop(self, black=True)
        self[6, 7] = Knight(self, black=True)
        self[7, 7] = Rock(self, black=True)

        self._white_to_move=True

    def __setitem__(self, key, value):
        """
        i, j = key
        i ... 0..7, it means a..h
        j ... 0..7, it means 1..8

        e.g. e4 is (4, 3)
        """
        i, j = key
        self._board[j*8+i] = value

    def __getitem__(self, key):
        i, j = key
        return self._board[j*8+i]

    def a2i(self, x):
        if x == "a": i = 0
        if x == "b": i = 1
        if x == "c": i = 2
        if x == "d": i = 3
        if x == "e": i = 4
        if x == "f": i = 5
        if x == "g": i = 6
        if x == "h": i = 7
        return i

    def parse_move(self, move):
        def convert_field(field):
            if len(field) == 2:
                x = field[0]
                y = field[1]
                i = self.a2i(x)
                j = int(y)-1
                return i, j
            else:
                print field
                raise InvalidMove()
        if move[0] == "R":
            piece = Rock
        elif move[0] == "N":
            piece = Knight
        elif move[0] == "B":
            piece = Bishop
        elif move[0] == "Q":
            piece = Queen
        elif move[0] == "K":
            piece = King
        else:
            piece = Pawn
        if piece != Pawn:
            move = move[1:]
        if move.find("x") != -1:
            capture = True
            move = move.replace("x", "")
        else:
            capture = False
        if move[-1] == "+":
            check = True
            move = move[:-1]
        else:
            check = False
        helper = move[:-2]
        move = move[-2:]
        field = convert_field(move)
        return piece, field, capture, check, helper

    def find_piece(self, piece, field):
        """
        Finds the piece "piece" that can go to the field "field".
        """
        candidates = []
        # first find all pieces of the type "piece" on the board:
        for i in range(8):
            for j in range(8):
                if isinstance(self[i, j], piece) and \
                        (self[i, j].white() == self._white_to_move):
                            candidates += [(i, j)]
        # try each of them:
        candidates = [x for x in candidates if self[x].can_move(x, field)]
        return candidates

    def use_helper(self, helper, candidates):
        if helper in "abcdefgh":
            i = self.a2i(helper)
            return [x for x in candidates if x[0] == i]
        return candidates

    def move_algebraic(self, move):
        """
        Do one move.

        "move" is given in the Short Algebraic notation.
        """
        if move == "O-O":
            # kingside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (6, 0), True)
                self.move_coordinate((7, 0), (5, 0))
            else:
                self.move_coordinate((4, 7), (6, 7), True)
                self.move_coordinate((7, 7), (5, 7))
        elif move == "O-O-O":
            # queenside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (2, 0), True)
                self.move_coordinate((0, 0), (3, 0))
            else:
                self.move_coordinate((4, 7), (2, 7), True)
                self.move_coordinate((0, 7), (3, 7))
        else:
            piece, field, capture, check, helper = self.parse_move(move)
            if capture:
                if self[field] is None:
                    raise InvalidMove()
            else:
                if self[field] is not None:
                    raise InvalidMove()
            possible_pieces = self.find_piece(piece, field)
            if len(possible_pieces) != 1:
                possible_pieces = self.use_helper(helper, possible_pieces)
            if len(possible_pieces) != 1:
                raise InvalidMove()
            self.move_coordinate(possible_pieces[0], field)

    def move_coordinate(self, old, new, castling=False):
        """
        Do one move. "old" and "new" are coordinates.

        Example:
        >>> b.move_coordinate((0, 0), (4, 0))
        """

        p = self[old]
        if p is None:
            raise InvalidMove()

        if not (self._white_to_move == (not p.black())):
            raise InvalidMove()

        self[old] = None
        self[new] = p
        if not castling:
            self._white_to_move = not self._white_to_move

    def to_ascii_art(self):
        s = ""
        s += "+" + "---+"*8 + "\n"
        for j in reversed(range(8)):
            row = "|"
            for i in range(8):
                if self[i, j] is not None:
                    if self[i, j].black():
                        row += "#%s#|" % self[i, j].to_ascii_art()
                    else:
                        row += " %s |" % self[i, j].to_ascii_art()
                else:
                    row += "   |"
            s += row + "\n"
            s += "+" + "---+"*8 + "\n"
        return s

    def to_string(self):
        s = ""
        for j in reversed(range(8)):
            for i in range(8):
                if self[i, j] is None:
                    s += " "
                else:
                    s += self[i, j].to_string()
        return s


    def __str__(self):
        return self.to_ascii_art()

class Piece(object):

    def __init__(self, board, black=False):
        self._board = board
        self._black = black

    def black(self):
        return self._black

    def white(self):
        return not self._black


class Rock(Piece):

    def to_ascii_art(self):
        return "R"

    def to_string(self):
        if self._black:
            return "R"
        else:
            return "r"

    def can_move(self, old, new):
        def r(a, b):
            """
            Returns the integers between a, b, exclusive.

            Example:
            >>> r(3, 7)
            [4, 5, 6]
            >>> r(7, 3)
            [4, 5, 6]
            """
            a, b = sorted([a, b])
            return range(a+1, b)
        dx = old[0]-new[0]
        dy = old[1]-new[1]
        if old[1] == new[1]:
            # x-movement
            # check that no piece is between the old and new position
            for i in r(old[0], new[0]):
                if self._board[i, old[1]] is not None:
                    return False
            return True
        if old[0] == new[0]:
            # y-movement
            # check that no piece is between the old and new position
            for j in r(old[1], new[1]):
                if self._board[old[0], j] is not None:
                    return False
            return True
        return False


class Knight(Piece):

    def to_ascii_art(self):
        return "N"

    def to_string(self):
        if self._black:
            return "N"
        else:
            return "n"

    def can_move(self, old, new):
        d = (old[0]-new[0])**2 + (old[1]-new[1])**2
        return d == 5

class Bishop(Piece):

    def to_ascii_art(self):
        return "B"

    def to_string(self):
        if self._black:
            return "B"
        else:
            return "b"

    def can_move(self, old, new):
        dx = old[0]-new[0]
        dy = old[1]-new[1]
        return (dx == dy) or (dx == -dy)

class Queen(Piece):

    def to_ascii_art(self):
        return "Q"

    def to_string(self):
        if self._black:
            return "Q"
        else:
            return "q"

class King(Piece):

    def to_ascii_art(self):
        return "K"

    def to_string(self):
        if self._black:
            return "K"
        else:
            return "k"

class Pawn(Piece):

    def to_ascii_art(self):
        return "p"

    def to_string(self):
        if self._black:
            return "P"
        else:
            return "p"

    def can_move(self, old, new):
        dx = new[0]-old[0]
        dy = new[1]-old[1]
        if dx == 0:
            if self._board[new] is None:
                if self.white():
                    return (dy == 1) or ((dy == 2) and (old[1] == 1))
                else:
                    return (dy == -1) or ((dy == -2) and (old[1] == 6))
        if dx in [-1, 1]:
            if self._board[new] is not None:
                if self.white():
                    return dy == 1
                else:
                    return dy == -1
        return False

def main():
    moves = ['e4', 'e5', 'Nf3', 'Nc6', 'Bb5', 'a6', 'Ba4', 'Nf6', 'O-O', 'Be7', 'Re1', 'b5', 'Bb3', 'd6', 'c3', 'O-O', 'h3', 'Nb8', 'd4', 'Nbd7', 'c4', 'c6', 'cxb5', 'axb5', 'Nc3', 'Bb7', 'Bg5', 'b4', 'Nb1', 'h6', 'Bh4', 'c5', 'dxe5', 'Nxe4', 'Bxe7', 'Qxe7', 'exd6', 'Qf6', 'Nbd2', 'Nxd6', 'Nc4', 'Nxc4', 'Bxc4', 'Nb6', 'Ne5', 'Rae8', 'Bxf7+', 'Rxf7', 'Nxf7', 'Rxe1+', 'Qxe1', 'Kxf7', 'Qe3', 'Qg5', 'Qxg5', 'hxg5', 'b3', 'Ke6', 'a3', 'Kd6', 'axb4', 'cxb4', 'Ra5', 'Nd5', 'f3', 'Bc8', 'Kf2', 'Bf5', 'Ra7', 'g6', 'Ra6+', 'Kc5', 'Ke1', 'Nf4', 'g3', 'Nxh3', 'Kd2', 'Kb5', 'Rd6', 'Kc5', 'Ra6', 'Nf2', 'g4', 'Bd3', 'Re6']
    print moves[20]
    moves = moves[:20]
    b = Board()
    for move in moves:
        b.move_algebraic(move)
    print b
    print b.to_string()

if __name__ == "__main__":
    main()
