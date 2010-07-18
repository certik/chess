class InvalidMove(Exception):
    pass

class Board(object):

    def __init__(self):
        self._board = [None]*64
        self.setup()
        self._moves = []

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

    def i2a(self, i):
        return "abcdefgh"[i]

    def parse_move(self, move):
        def convert_field(field):
            if len(field) == 2:
                x = field[0]
                y = field[1]
                i = self.a2i(x)
                j = int(y)-1
                return i, j
            else:
                raise InvalidMove(move)
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
        if (helper != "") and (helper in "abcdefgh"):
            i = self.a2i(helper)
            return [x for x in candidates if x[0] == i]
        if (helper != "") and (helper in "12345678"):
            j = int(helper) - 1
            return [x for x in candidates if x[1] == j]
        return candidates

    def moves_from_list(self, moves):
        for move in moves:
            self.move_algebraic(move)

    def move_algebraic(self, move):
        """
        Do one move.

        "move" is given in the Short Algebraic notation.
        """
        if move == "O-O":
            # kingside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (6, 0))
                self.move_coordinate((7, 0), (5, 0), True)
            else:
                self.move_coordinate((4, 7), (6, 7))
                self.move_coordinate((7, 7), (5, 7), True)
        elif move == "O-O-O":
            # queenside castling
            if self._white_to_move:
                self.move_coordinate((4, 0), (2, 0))
                self.move_coordinate((0, 0), (3, 0), True)
            else:
                self.move_coordinate((4, 7), (2, 7))
                self.move_coordinate((0, 7), (3, 7), True)
        else:
            piece, field, capture, check, helper = self.parse_move(move)
            if capture:
                if self[field] is None:
                    if (piece == Pawn) and (field[1] in [2, 5]):
                        # this is probably en passant, so ok
                        pass
                    else:
                        raise InvalidMove(move)
            else:
                if self[field] is not None:
                    raise InvalidMove(move)
            possible_pieces = self.find_piece(piece, field)
            if len(possible_pieces) != 1:
                possible_pieces = self.use_helper(helper, possible_pieces)
            if len(possible_pieces) != 1:
                raise InvalidMove(move)
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

        if not castling:
            if not (self._white_to_move == (not p.black())):
                raise InvalidMove()

        self[old] = None
        self[new] = p
        # en passant:
        if isinstance(p, Pawn):
            if self._white_to_move:
                b = self[new[0], 4]
                if (new[1] == 5) and isinstance(b, Pawn) and b.black():
                    self[new[0], 4] = None
            else:
                b = self[new[0], 3]
                if (new[1] == 2) and isinstance(b, Pawn) and b.white():
                    self[new[0], 3] = None
        if not castling:
            self._white_to_move = not self._white_to_move
            move = "%s%d%s%d" % (self.i2a(old[0]), old[1]+1,
                    self.i2a(new[0]), new[1]+1)
            self._moves.append(move)

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

    def get_moves(self):
        """
        Return a list of moves in "e2e4" notation.
        """
        return self._moves

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

    def can_move(self, old, new):
        return Bishop(self._board, self._black).can_move(old, new) or \
                Rock(self._board, self._black).can_move(old, new)

class King(Piece):

    def to_ascii_art(self):
        return "K"

    def to_string(self):
        if self._black:
            return "K"
        else:
            return "k"

    def can_move(self, old, new):
        dx = old[0]-new[0]
        dy = old[1]-new[1]
        return (dx in [-1, 0, 1]) and (dy in [-1, 0, 1])

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
            else:
                # check for en passant:
                if self.white():
                    b = self._board[new[0], 4]
                    if (new[1] == 5) and isinstance(b, Pawn) and b.black():
                        return True
                else:
                    b = self._board[new[0], 3]
                    if (new[1] == 2) and isinstance(b, Pawn) and b.white():
                        return True
        return False

def main():
    moves = ['d4', 'Nf6', 'c4', 'c5', 'd5', 'b5', 'cxb5', 'a6', 'e3', 'Bb7', 'Nc3', 'axb5', 'Bxb5', 'Qa5', 'Bd2', 'Qb6', 'Nf3', 'Nxd5', 'Nxd5', 'Bxd5', 'a4', 'e6', 'Bc3', 'Be7', 'O-O', 'O-O', 'Ne5', 'd6', 'Nc4', 'Bxc4', 'Qg4', 'g6', 'Qxc4', 'Nc6', 'e4', 'Nd4', 'Bxd4', 'cxd4', 'Rfc1', 'Bg5', 'Rc2', 'Kg7', 'b4', 'Rfc8', 'Qxc8', 'Rxc8', 'Rxc8', 'd3', 'Bxd3', 'Qd4', 'Rd1', 'Qxb4', 'Bc2', 'Bf6', 'h3', 'Bd4', 'Rf1', 'Bc5', 'Ra8', 'h5', 'a5', 'Qb7', 'Re8', 'Qa6', 'Bd1', 'Qxa5', 'Bf3', 'h4', 'Re7', 'Qb4', 'Rc7', 'Qb6', 'Rc8', 'Qb7', 'Re8', 'Qb2', 'Bd1', 'Qd2', 'Bf3', 'Qd4', 'Ra8', 'Kf6', 'Ra2', 'Qe5', 'Rc1', 'Qf4', 'Rc4', 'Ke5', 'Re2', 'Qg5', 'Kf1', 'Qd8', 'Rcc2', 'Qa5', 'Ra2', 'Qc3', 'Rac2', 'Qd3', 'Kg1', 'Qd1+', 'Kh2', 'Qa1', 'Ra2', 'Qc3', 'Rec2', 'Qd4', 'Rd2', 'Qc3', 'Rdc2', 'Qe1', 'Re2', 'Qb1', 'Rac2', 'Bd4', 'Rcd2', 'Qb4', 'Rc2', 'Kf6', 'g3', 'hxg3+', 'Kxg3', 'Be5+', 'Kg2', 'Qb8', 'h4', 'Qh8', 'Kh3', 'Qh6', 'Re1', 'Qf4', 'Kg2', 'Qh2+', 'Kf1', 'Qxh4', 'Rd1', 'Qh8', 'Ke2', 'Qb8', 'Rcd2', 'Qb5+', 'Rd3', 'Qc4', 'Rg1', 'Bf4', 'Rgd1', 'Ke5', 'Ke1', 'Kf6', 'Rd4', 'Qc3+', 'Ke2', 'Qc2+', 'Kf1', 'Kg5', 'Be2', 'f5', 'f3', 'Qc3', 'R1d3', 'Qc7', 'Bd1', 'Qh7', 'exf5', 'Qh1+', 'Kf2', 'Qh2+', 'Kf1', 'gxf5', 'Bb3', 'Bg3', 'f4+', 'Kf6', 'Rd2', 'Qh1+', 'Ke2', 'Qg2+', 'Kd3', 'Qf3+', 'Kc2', 'Bxf4', 'Rd1', 'Qe2+', 'Kb1', 'Be5', 'R4d2', 'Qe4+', 'Rd3', 'd5', 'Bc2', 'Qb4+', 'Rb3', 'Qa5', 'Kc1', 'Qa1+', 'Kd2', 'Qd4+', 'Kc1', 'Qc5', 'Rf1', 'Bd4', 'Kd2', 'Qc4', 'Rff3', 'Be5', 'Kd1', 'Bd6', 'Rbc3', 'Qg4', 'Ke2', 'f4', 'Kf1', 'Bc5', 'Ke2', 'Bd6', 'Bb3', 'Be5', 'Rcd3', 'Bd6', 'Kf1', 'Bc5', 'Ke1', 'Ke5', 'Kd2', 'Be3+', 'Rdxe3+', 'fxe3+', 'Rxe3+', 'Kd6', 'Bc2', 'e5', 'Ke1', 'e4', 'Kd2', 'Ke5', 'Re2', 'Qf3', 'Bd1', 'd4', 'Kc1', 'Qc3+', 'Kb1', 'd3', 'Rh2', 'Kd4', 'Ka2', 'Qa5+', 'Kb2', 'Qc3+', 'Ka2', 'Qc1', 'Rh8', 'Qxd1', 'Ka3', 'Qb1', 'Rd8+', 'Ke3'] 
    b = Board()
    b.moves_from_list(moves)
    print b
    print '"' + b.to_string() + '"'

if __name__ == "__main__":
    main()
