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
    STATUS_WIN = '{} wins!'
    STATUS_GAME_IN_PROGRESS = 'Game in progress.'
    VALID_COORDINATE = r'^[ABC][123]$'
    VALID_SIGN = r'^[' + X_SIGN + O_SIGN + r']$'
    LINE = '  -------------\n'
    ROW = '{} | {} | {} | {} |\n'
    END_ROW = '    A   B   C  \n'
    COLUMNS = {'A': 0, 'B': 1, 'C': 2}
    BOARD_SIZE = 3

    def __init__(self):
        self._board = [[self.EMPTY_SIGN] * self.BOARD_SIZE
                       for row_num in range(self.BOARD_SIZE)]
        self._last_played = None
        self._status = self.STATUS_GAME_IN_PROGRESS
        self._moves_count = 0

    @staticmethod
    def _get_board_coords(key):
        row = TicTacToeBoard.BOARD_SIZE - int(key[1])
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
        self._moves_count += 1

        if (self._status == self.STATUS_GAME_IN_PROGRESS and
                self._move_wins(row, col, value)):
            self._status = self.STATUS_WIN.format(value)

        if (self._moves_count == self.BOARD_SIZE ** 2 and
                self._status == self.STATUS_GAME_IN_PROGRESS):
            self._status = self.STATUS_DRAW

    def _move_wins(self, row, col, value):
        if all(map(lambda x: x == value, self._get_row(row))):
            return True
        if all(map(lambda x: x == value, self._get_col(col))):
            return True

        if (row == col and
                all(map(lambda x: x == value, self._get_diagonal(True)))):
            return True

        if (row == self.BOARD_SIZE - 1 - col and
                all(map(lambda x: x == value, self._get_diagonal(False)))):
            return True

        return False

    def _get_row(self, row_num):
        return self._board[row_num]

    def _get_col(self, col_num):
        return [row[col_num] for row in self._board]

    def _get_diagonal(self, main_diagonal=True):
        if main_diagonal:
            return [self._board[row_num][row_num]
                    for row_num in range(self.BOARD_SIZE)]
        else:
            return [self._board[row_num][self.BOARD_SIZE - 1 - row_num]
                    for row_num in range(self.BOARD_SIZE)]

    def game_status(self):
        return self._status

    def __str__(self):
        result = '\n'
        for row in range(self.BOARD_SIZE):
            result += self.LINE
            result += self.ROW.format(self.BOARD_SIZE - row, *self._board[row])

        result += self.LINE
        result += self.END_ROW
        return result
