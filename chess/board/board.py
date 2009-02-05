class InvalidMove(Exception):
    pass

class Board(object):

    def __init__(self):
        self._board = [None]*64
        self.setup()

    def setup(self):
        self[0, 0] = Rock()
        self[1, 0] = Knight()
        self[2, 0] = Bishop()
        self[3, 0] = Queen()
        self[4, 0] = King()
        self[5, 0] = Bishop()
        self[6, 0] = Knight()
        self[7, 0] = Rock()

        for i in range(8):
            self[i, 1] = Pawn()
            self[i, 6] = Pawn(black=True)

        self[0, 7] = Rock(black=True)
        self[1, 7] = Knight(black=True)
        self[2, 7] = Bishop(black=True)
        self[3, 7] = Queen(black=True)
        self[4, 7] = King(black=True)
        self[5, 7] = Bishop(black=True)
        self[6, 7] = Knight(black=True)
        self[7, 7] = Rock(black=True)

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
        if piece == Pawn:
            field = convert_field(move)
        else:
            field = convert_field(move[1:])
        capture = False
        check = False
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
        candidates = [x for x in candidates if piece.can_move(x, field)]
        return candidates

    def move_algebraic(self, move):
        """
        Do one move.

        "move" is given in the Short Algebraic notation.
        """
        if move == "O-O":
            # kingside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (6, 0))
            else:
                self.move_coordinate((4, 7), (6, 7))
        elif move == "O-O-O":
            # queenside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (2, 0))
            else:
                self.move_coordinate((4, 7), (2, 7))
        else:
            piece, field, capture, check = self.parse_move(move)
            possible_pieces = self.find_piece(piece, field)
            print possible_pieces
            if len(possible_pieces) != 1:
                raise InvalidMove()
            self.move_coordinate(possible_pieces[0], field)

    def move_coordinate(self, old, new):
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


    def __str__(self):
        return self.to_ascii_art()

class Piece(object):

    def __init__(self, black=False):
        self._black = black

    def black(self):
        return self._black

    def white(self):
        return not self._black


class Rock(Piece):

    def to_ascii_art(self):
        return "R"

class Knight(Piece):

    def to_ascii_art(self):
        return "N"

    @classmethod
    def can_move(cls, old, new):
        d = (old[0]-new[0])**2 + (old[1]-new[1])**2
        return d == 5

class Bishop(Piece):

    def to_ascii_art(self):
        return "B"

class Queen(Piece):

    def to_ascii_art(self):
        return "Q"

class King(Piece):

    def to_ascii_art(self):
        return "K"

class Pawn(Piece):

    def to_ascii_art(self):
        return "p"

def main():
    b = Board()
    print b
    b.move_coordinate((4, 1), (4, 3))
    print b
    b.move_coordinate((4, 6), (4, 4))
    print b
    b.move_algebraic("Nf3")
    b.move_algebraic("Nc6")
    #b.move_algebraic("Bb5")
    print b

if __name__ == "__main__":
    main()
