"""
Authors: Yang Liu (yliu17), Tyler Nickerson (tjnickerson)
Date: Jan 28, 2016
"""
import csv
import sys
import os.path

import numpy as np
from features import Detector

DEBUG = 0
BOARD_HEIGHT = 6
BOARD_WIDTH = 7


def main():
    # Read command line arguments
    args = sys.argv[1:]
    # More than 1 argument supplied
    if len(args) > 1:
        # Get data filename
        input_filename = args[0]
        output_filename = args[1]
        # Read each line of input file and add to the examples and output lists
        if os.path.isfile(input_filename):
            feature_headers = []
            with open(input_filename, 'rb') as csvfile:
                header = csvfile.readline()
                output = header
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
                        board_row.append(int(i))
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

                    # Update feature headers (names)
                    features = Detector(board).allFeatures()
                    feature_headers = features.keys()

                    # Add line to output with feature values appended
                    output += ','.join(row) + ',' + winner + \
                              ',' + \
                        ','.join(map(str, features.values())) + '\n'

            # Will be used to get the first line of the file
            first_newline = output.find('\n')

            # Append new feature titles to header line
            output = output[:first_newline][:-1] + ',' + \
                ','.join(feature_headers) + \
                output[first_newline:]

            # Write the output to file
            with open(output_filename, 'wb') as output_file:
                output_file.write(output)
        else:
            # Throw error when cannot open file
            print("Input file does not exist.")
    else:
        # Show usage when not providing enough argument
        print("Usage: python features.py <input filename> <output filename>")

if __name__ == "__main__":
    main()
