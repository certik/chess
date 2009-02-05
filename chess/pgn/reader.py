"""
Chess PGN file reader.
"""

from grammar import parse_pgn
import pyparsing

class PGNReader(object):

    def __init__(self, text):
        """
        Imports the PGN file given as a string in "text".
        """

        d = self.import_pgn(text)
        self._moves = d["moves"]
        self._header = d["header"]
        self._result = d["result"]
        self._white = d["header"].get("White", "")
        self._black = d["header"].get("Black", "")

    def import_pgn(self, text):
        """
        Parses the text and returns a dictionary, which represents the pgn
        file.
        """
        header, moves, end = parse_pgn(text)
        return {"header": dict(list(header)), "moves": moves, "result": end[0]}

    def moves2str(self, moves):
        s = ""
        for n, move in enumerate(moves):
            if len(move) == 2:
                s += "%d. %s %s\n" % (n+1, move[0], move[1])
            else:
                assert len(move) == 1
                s += "%d. %s\n" % (n+1, move[0])
        return s

    def moves_as_list(self):
        l = []
        for move in self._moves:
            if len(move) == 2:
                l += [move[0], move[1]]
            else:
                assert len(move) == 1
                l += [move[0]]
        return l

    def __str__(self):
        s = "%s - %s\n%s%s" % (self._white, self._black,
            self.moves2str(self._moves), self._result)
        return s
