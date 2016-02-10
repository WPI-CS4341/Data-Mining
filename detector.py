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
        # For each row on the board
        for y in xrange(len(self.board)):
            x = 0
            is_connect = False
            checker_count = 0
            row = self.board[y]
            # Iterate through the cells
            while x < len(row):
                # If we are not at the bottom of the board and there is no
                # supporting cell beneath this one...
                if y != len(self.board) - 1 and self.board[y + 1][x] == EMPTY_CELL:
                    # ...skip it
                    x += 1
                else:
                    # Increment count for every player checker we find
                    if row[x] == player:
                        checker_count += 1
                    elif row[x] == EMPTY_CELL:
                        if checker_count > 1:
                            player_moves += 1
                        checker_count = 0
                    else:
                        checker_count = 0

                    if x == len(row) - 1:
                        if checker_count > 1 and \
                            x - (checker_count + 1) >= 0 and \
                                row[x - (checker_count + 1)] == EMPTY_CELL:
                                player_moves += 1
                                checker_count = 0

                    x += 1
        return player_moves

    def __verticalMoveCount(self, player):
        player_moves = 0
        # Transpose and flip the board matrix for iteration
        for row in np.fliplr(self.board.T):
            checker_count = 0
            for i in xrange(len(row)):
                if row[i] == player:
                    checker_count += 1
                elif row[i] == EMPTY_CELL:
                    if checker_count > 1:
                        player_moves += 1
                    checker_count = 0
                else:
                    checker_count = 0
                if i == len(row) - 1:
                    if checker_count > 1:
                        player_moves += 1
                        checker_count = 0
        return player_moves

    def __horizontalSequenceCount(self, player):
        player_moves = 0
        # For each row on the board
        for y in xrange(len(self.board)):
            x = 0
            is_sequence = False
            row = self.board[y]
            # Iterate through the cells
            while x < len(row):
                # If we're not on the bottom row and there is no supporting
                # cell beneath this one...
                if y != len(self.board) - 1 and self.board[y + 1][x] == EMPTY_CELL:
                    # ...we skip it
                    x += 1
                else:
                    # If we're not at the board's edge...
                    if x != len(row) - 1:
                        # ...and an empty cell comes after the current one...
                        if (row[x] == player and row[x + 1] == EMPTY_CELL):
                            # ...and the cell after the empty cell has the current player's checker...
                            if (x + 2 <= len(row) - 1 and row[x + 2] == player):
                                # ...it is a sequence
                                is_sequence = True
                x += 1
            # If there is a sequence...
            if is_sequence:
                # ...increment the move counter
                player_moves += 1
        return player_moves

    # PUBLIC METHODS

    def allFeatures(self):
        return {
            'leftCornerPlayer': self.leftCornerPlayer(),
            'centerPlayer': self.centerPlayer(),
            'openMoves': self.openMoves(),
            'openSequences': self.openSequences(),
            'winReach': self.predictedWinner()
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
    Returns the the difference in open moves between players
    If the value is negative, player 1 is in the lead
    If the value is positive, player 2 is in the lead
    """

    def openMoves(self):
        total_moves = []

        for player in [PLAYER_1, PLAYER_2]:
            player_horizontal_moves = self.__horizontalMoveCount(player)
            player_vertical_moves = self.__verticalMoveCount(player)
            total_moves.append(player_vertical_moves)
        return total_moves[1] - total_moves[0]

    """
    Returns the difference in open sequences (sequences
    that have gaps in the middle) between players
    If the value is negative, player 1 is in the lead
    If the value is positive, player 2 is in the lead
    """

    def openSequences(self):
        total_moves = []

        for player in [PLAYER_1, PLAYER_2]:
            total_moves.append(self.__horizontalSequenceCount(player))
        return total_moves[1] - total_moves[0]

    """
    Returns a value representing how far away a board is from being won (the higher the number, the closer it is)
    """

    def predictedWinner(self):
        return 0
