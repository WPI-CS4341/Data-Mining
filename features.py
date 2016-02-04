"""
Authors: Yang Liu (yliu17), Tyler Nickerson (tjnickerson)
Date: Jan 28, 2016
"""
import csv
import sys
import os.path

import numpy as np

DEBUG = 0
BOARD_HEIGHT = 6
BOARD_WIDTH = 7

def parse_file(filename):
    """Parse the input file as a board state"""
    # Stores the board as a matrix
    boards = []

    # Read each line and add to the examples and output lists
    if os.path.isfile(filename):
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                # Initialize empty board matrix
                board = []

                # Get the winner and remove it from the list
                winner = row.pop(len(row) - 1)

                # The current row and column
                board_column = 0
                board_row = []

                # Iterate through the input data
                for i in row:
                    board_row.append(i)
                    # If we've filled a row, move onto the next one
                    if board_column == BOARD_HEIGHT - 1:
                        board.append(board_row)
                        board_column = 0
                        board_row = []
                    # Otherwise we push the value into the column
                    else:
                        board_column += 1

                # Add board to the collection of boards
                board = np.flipud(np.array(board).T)
                boards.append(board)
    else:
        # Throw error when cannot open file
        print("Input file does not exist.")

    # Return the inputs and outputs
    return np.array(boards)

def main():
    # Read command line arguments
    args = sys.argv[1:]
    # More than 1 argument supplied
    if len(args) > 0:
        # Get data filename
        filename = args[0]
        # Set default number of hidden nodes to 5
        hidden_layer_size = 5
        # Set default hold out data to 20%
        percentage = 0.20
        # When node number or supplied
        # if len(args) > 3:
        #     if args[1] == "h":
        #         # Set up number of nodes in the hidden layer
        #         hidden_layer_size = int(args[2])
        #         if len(args) > 3:
        #             if args[3] == "p":
        #                 # Setup hold out percentage
        #                 percentage = float(args[4])
        #     elif args[1] == "p":
        #         # Setup hold out percentage
        #         percentage = float(args[2])

        # Read data into memory
        board = parse_file(filename)

        # Train only when there is data
        print board

        # if (board.any()):
        # else:
            # Do nothing when no data supplied
            # print("No data to train and test the network")
    else:
        # Show usage when not providing enough argument
        print("Usage: python ann.py <filename> [h <number of hidden nodes> | p <holdout percentage>]")

if __name__ == "__main__":
    main()
