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

    def parse_move(self, move):
        def convert_field(field):
            if len(field) == 2:
                x = field[0]
                y = field[1]
                if x == "a": i = 0
                if x == "b": i = 1
                if x == "c": i = 2
                if x == "d": i = 3
                if x == "e": i = 4
                if x == "f": i = 5
                if x == "g": i = 6
                if x == "h": i = 7
                j = int(y)-1
                return i, j
            else:
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
        if move[0] == "x":
            capture = True
            move = move[1:]
        else:
            capture = False
        if move[-1] == "+":
            check = True
            move = move[:-1]
        else:
            check = False
        field = convert_field(move)
        return piece, field, capture, check

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
            piece, field, capture, check = self.parse_move(move)
            if capture:
                if self[field] is None:
                    raise InvalidMove()
            else:
                if self[field] is not None:
                    raise InvalidMove()
            possible_pieces = self.find_piece(piece, field)
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
        if dx != 0:
            return False
        if self.white():
            return (dy == 1) or ((dy == 2) and (old[1] == 1))
        else:
            return (dy == -1) or ((dy == -2) and (old[1] == 6))

def main():
    b = Board()
    print b
    b.move_algebraic("e4")
    b.move_algebraic("e5")
    b.move_algebraic("Nf3")
    b.move_algebraic("Nc6")
    b.move_algebraic("Bb5")
    b.move_algebraic("a6")
    b.move_algebraic("Bxc6")
    b.move_algebraic("d6")
    b.move_algebraic("d3")
    b.move_algebraic("Bb4+")
    b.move_algebraic("Nc3")
    b.move_algebraic("Nf6")
    b.move_algebraic("O-O")
    b.move_algebraic("Bxc3")
    b.move_algebraic("Re1")
    print b
    print b.to_string()

if __name__ == "__main__":
    main()
