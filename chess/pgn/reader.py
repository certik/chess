from grammar import parse_pgn
import pyparsing

class PGNReader(object):

    def __init__(self, text):
        """
        Imports the PGN file given as a string in "text".
        """

        d = self.import_pgn(text)
        self._moves = d["moves"]
        print d["header"]
        print d["end"]

    def import_pgn(self, text):
        """
        Parses the text and returns a dictionary, which represents the pgn
        file.
        """
        header, moves, end = parse_pgn(text)
        return {"header": dict(list(header)), "moves": moves, "end": end[0]}

    def __str__(self):
        return str(self._moves)
