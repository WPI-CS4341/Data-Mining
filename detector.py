import numpy as np

PLAYER_1 = 1
PLAYER_2 = 2
EMPTY_CELL = 0


class Detector(object):

    def __init__(self, board):
        self.board = board

    # PRIVATE METHODS

    def __checkForConnect(self, cells, player):
        is_connect = False
        for i in xrange(0, len(cells) - 1):
            if i != len(cells) - 1:
                if cells[i] == player and cells[i + 1] == player:
                    if (i != 0 and cells[i - 1] == EMPTY_CELL) or \
                       (i + 2 < len(cells) - 1 and cells[i + 2] == EMPTY_CELL):
                        is_connect = True
        return is_connect

    def __checkForBlockable(self, cells, player):
        is_blockable = False
        for i in xrange(0, len(cells) - 1):
            if i != len(cells) - 1:
                if cells[i] == player and cells[i + 1] == 0:
                    if (i + 2 < len(cells) - 1 and cells[i + 2] == player):
                        is_blockable = True
        return is_blockable

    def __horizontalMoveCount(self, player):
        player_moves = 0
        for row in self.board:
            if self.__checkForConnect(row, player):
                player_moves += 1
        return player_moves

    def __verticalMoveCount(self, player):
        player_moves = 0
        for row in self.board.T:
            if self.__checkForConnect(row, player):
                player_moves += 1
        return player_moves

    def __diagonalMoveCount(self, player, reverse=False):
        board = np.flipud(self.board) if reverse else self.board
        i = 0
        main_diagonal = np.diag(board)
        player_moves = 0

        while(len(main_diagonal) != 0):
            diag_a = np.diag(board, i)
            diag_b = np.diag(board, -i)

            if self.__checkForConnect(diag_a, player) or \
               self.__checkForConnect(diag_b, player):
                player_moves += 1

            i += 1
            main_diagonal = np.diag(board, i)

        return player_moves

    def __horizontalBlockCount(self, player):
        player_moves = 0
        for row in self.board:
            if self.__checkForBlockable(row, player):
                player_moves += 1
        return player_moves

    def __verticalBlockCount(self, player):
        player_moves = 0
        for row in self.board.T:
            if self.__checkForBlockable(row, player):
                player_moves += 1
        return player_moves

    def __diagonalBlockCount(self, player, reverse=False):
        board = np.flipud(self.board) if reverse else self.board
        i = 0
        main_diagonal = np.diag(board)
        player_moves = 0

        while(len(main_diagonal) != 0):
            diag_a = np.diag(board, i)
            diag_b = np.diag(board, -i)

            if self.__checkForBlockable(diag_a, player) or \
               self.__checkForBlockable(diag_b, player):
                player_moves += 1

            i += 1
            main_diagonal = np.diag(board, i)

        return player_moves

    # PUBLIC METHODS

    def allFeatures(self):
        return {
            'leftCornerPlayer': self.leftCornerPlayer(),
            'centerPlayer': self.centerPlayer(),
            'diffMoves': self.diffMoves(),
            'blockableMoves': self.blockableMoves(),
            'winReach': self.winReach()
        }

    """
    Returns the player in the lefthand corner of the board
    Returns 0 if there is no player there
    """
    def leftCornerPlayer(self):
        return self.board[len(self.board) - 1][0]

    """
    Returns the player with the most moves in the center of the board
    (i.e. not on the left or right edges)
    Returns 0 if neither player is in the center of the board
    """
    def centerPlayer(self):
        player1_count = 0
        player2_count = 0
        for row in self.board:
            for column in xrange(1, len(self.board) - 2):
                cell = row[column]
                if cell == PLAYER_1:
                    player1_count += 1
                elif cell == PLAYER_2:
                    player2_count += 1
        return PLAYER_1 if player1_count > player2_count else PLAYER_2

    """
    Returns the difference in moves between the two players
    """
    def diffMoves(self):
        total_moves = []

        for player in [PLAYER_1, PLAYER_2]:
            player_diagonal_moves = self.__diagonalMoveCount(player) + self.__diagonalMoveCount(player, True)
            player_horizontal_moves = self.__horizontalMoveCount(player)
            player_vertical_moves = self.__verticalMoveCount(player)
            total_moves.append(player_diagonal_moves + player_horizontal_moves + player_vertical_moves)

        return np.amax(total_moves) - np.amin(total_moves)

    """
    Returns number of moves which have the potential to be blocked (have an open end)
    """
    def blockableMoves(self):
        total_moves = []

        for player in [PLAYER_1, PLAYER_2]:
            total_moves.append(self.__diagonalBlockCount(player) +
                               self.__diagonalBlockCount(player, True) +
                               self.__verticalBlockCount(player) +
                               self.__horizontalBlockCount(player)
                               )
        return np.sum(total_moves)
    """
    Returns a value representing how far away a board is from being won (the higher the number, the closer it is)
    """
    def winReach(self):
        return self.diffMoves() - self.blockableMoves()
