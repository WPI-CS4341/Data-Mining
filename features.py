"""
Authors: Yang Liu (yliu17), Tyler Nickerson (tjnickerson)
Date: Jan 28, 2016
"""
import sys
import os.path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

DEBUG = 0

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
        if len(args) > 3:
            if args[1] == "h":
                # Set up number of nodes in the hidden layer
                hidden_layer_size = int(args[2])
                if len(args) > 3:
                    if args[3] == "p":
                        # Setup hold out percentage
                        percentage = float(args[4])
            elif args[1] == "p":
                # Setup hold out percentage
                percentage = float(args[2])

        # Read data into memory
        examples, outputs = parse_file(filename)

        # Train only when there is data
        if (examples.any() and outputs.any()):
            # Split out the training set and test set
            percentage = int(round(len(examples) * percentage))
            testing = examples[:percentage]
            testing_output = outputs[:percentage]
            training = examples[percentage:]
            training_output = outputs[percentage:]

            # Initilize instance of the network
            ann = Artificial_Neural_Network(
                len(training[0]),
                hidden_layer_size,
                len(training_output[0])
            )

            # Train the network
            ann.train(training, training_output)
            # Test the network
            ann.test(testing, testing_output, True)
        else:
            # Do nothing when no data supplied
            print("No data to train and test the network")
    else:
        # Show usage when not providing enough argument
        print("Usage: python ann.py <filename> [h <number of hidden nodes> | p <holdout percentage>]")

if __name__ == "__main__":
    main()
