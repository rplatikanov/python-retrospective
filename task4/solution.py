import re


class InvalidMove(Exception):
    pass


class InvalidValue(Exception):
    pass


class InvalidKey(Exception):
    pass


class NotYourTurn(Exception):
    pass


class TicTacToeBoard:
    X_SIGN = 'X'
    O_SIGN = 'O'
    EMPTY_SIGN = ' '
    STATUS_DRAW = 'Draw!'
    STATUS_X_WINS = 'X wins!'
    STATUS_O_WINS = 'O wins!'
    STATUS_GAME_IN_PROGRESS = 'Game in progress.'
    VALID_COORDINATE = r'^[ABC][123]$'
    VALID_SIGN = r'^[' + X_SIGN + O_SIGN + r']$'
    LINE = '  -------------\n'
    ROW = '{} | {} | {} | {} |\n'
    END_ROW = '    A   B   C  \n'
    COLUMNS = {'A': 0, 'B': 1, 'C': 2}

    def __init__(self):
        self._board = [None] * 3
        for row in range(3):
            self._board[row] = [self.EMPTY_SIGN] * 3
        self._last_played = None
        self._status = self.STATUS_GAME_IN_PROGRESS

    @staticmethod
    def _get_board_coords(key):
        row = 3 - int(key[1])
        col = TicTacToeBoard.COLUMNS[key[0]]
        return row, col

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise InvalidKey

        matched_key = re.match(self.VALID_COORDINATE, key)
        if not matched_key:
            raise InvalidKey

        row, col = self._get_board_coords(key)
        return self._board[row][col]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise InvalidKey
        if not isinstance(value, str):
            raise InvalidValue

        matched_key = re.match(self.VALID_COORDINATE, key)
        matched_value = re.match(self.VALID_SIGN, value)
        if not matched_key:
            raise InvalidKey
        if not matched_value:
            raise InvalidValue

        if self._last_played is not None and self._last_played == value:
            raise NotYourTurn

        if self[key] != self.EMPTY_SIGN:
            raise InvalidMove

        self._last_played = value
        row, col = self._get_board_coords(key)
        self._board[row][col] = value

    def __str__(self):
        result = '\n'
        for row in range(3):
            result += self.LINE
            result += self.ROW.format(3 - row, *self._board[row])

        result += self.LINE
        result += self.END_ROW
        return result

    @staticmethod
    def _list_wins(list_):
        win_list_x = [TicTacToeBoard.X_SIGN] * 3
        win_list_o = [TicTacToeBoard.O_SIGN] * 3

        if list_ == win_list_x:
            return TicTacToeBoard.STATUS_X_WINS
        elif list_ == win_list_o:
            return TicTacToeBoard.STATUS_O_WINS

    def game_status(self):
        if self._status != self.STATUS_GAME_IN_PROGRESS:
            return self._status

        for row in self._board:
            win_test = self._list_wins(row)
            if win_test is not None:
                self._status = win_test
                return win_test

        cols = [[row[col] for row in self._board] for col in range(3)]

        for col in cols:
            win_test = self._list_wins(col)
            if win_test is not None:
                self._status = win_test
                return win_test

        diagonals = [[], []]
        for row in range(3):
            diagonals[0] += self._board[row][row]
            diagonals[1] += self._board[row][2 - row]

        for diagonal in diagonals:
            win_test = self._list_wins(diagonal)
            if win_test is not None:
                self._status = win_test
                return win_test

        for row in self._board:
            if self.EMPTY_SIGN in row:
                return self.STATUS_GAME_IN_PROGRESS

        self._status = self.STATUS_DRAW
        return self.STATUS_DRAW
