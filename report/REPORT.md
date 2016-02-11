# Data Mining With Python and Weka
_By Yang Liu & Tyler Nickerson_

For this project, a small program was written in Python 2.7 to extract feature data from sets of integers representing Connect-4 game board states (for more info on these strings, [click here](dataDescription.md)). These features were then plugged into [Weka 3](http://www.cs.waikato.ac.nz/ml/weka/), a Java program by New Zealand's [University of Waikato](http://www.waikato.ac.nz) that runs machine learning algorithms on sets of data. In this particular experiment, the feature was data was used to train/build both a neural network and a decision tree.

## The Features
As previously stated, each string (line) of input data is interpreted as a Connect-4 board state and loaded into a NumPy matrix. Using NumPy matrix operations, each board state is analyzed and five state features are produced for use in Weka. Those features as follows:

### leftCornerPlayer
#### Description
Returns the number of whichever player is in the left-hand corner of the board. While not entirely useful, this feature acts primarily as a benchmark and does not have a significant impact on the rest of the features.

#### Strategy
This feature was chosen as a benchmark to measure how a poor feature would perform during Weka testing.

### centerPlayer
#### Description
Returns the difference in the number of checkers by each player in the center of the board (no checkers along the left or right edges). If the value is positive, player1 has more tiles in the center. If the value is negative, player2 has more tiles.

#### Strategy
This feature was to chosen in order to provide insight as to which player currently has control of the board.

### openMoves <a id="openm"></a>
#### Description
Returns the difference in "open" moves between players (i.e moves in which another checker may be added to left or right side of the sequence). If the value returned is *positive*, then player one has made more "open" moves than player two. If the value is *negative*, then the opposite is true. The larger the absolute value of the returned integer, the greater the difference in moves. openMoves is computed by checking all horizontal and vertical moves and counting the strings of same-player checkers that have open spaces on either end. The returned value is the player two count subtracted from the player one count.

#### Strategy
This feature was chosen in order to measure player strategy. A higher absolute value for openMoves suggests that the player is able to freely make open moves without their opponent blocking them. As a result, this feature measures more of the opponent's strategy than the strategy of the player at hand. This is unlike [unblockableMoves](#unblockableMoves), which measures how strategic the current player is making "un-blockable" moves.

### openSequences <a id="opens"></a>
#### Description
Returns the difference in "open" checker sequences between players (i.e. sequences of checkers with gaps in the middle, allowing moves to be blocked). Similar to openMoves, player 1 has more "open" sequences on the board than player 2 if the difference is positive. The opposite holds true if the returned difference is negative. openSequences is calculated by checking all horizontal and vertical moves and seeing if there are gaps in any of the move sequences. In other words, every open space is analyzed using the following criteria:

* Is there "ground" below the space for a player to make a move (i.e. another checker or the bottom of the board)?

* Are the checkers to the left and right of the space are both of the same player?

If both of the above questions answer yes, then the sequence is "open". The count for player two is then subtracted from the count for player one and the difference is returned.

#### Strategy
This feature was chosen in order to again measure the strategy of the players. However, unlike [openMoves](#openm), which measures the opponent's basic ability to block moves, openSequences measures the opponent's ability in blocking moves which consist of two parts (a "front" and a "back"). This is representative of their ability to see the "big picture", so-to-speak, instead of blocking moves in a very quick, almost reflex-based fashion. If the difference is lower, than the opponent has a fairly good blocking strategy. If it is lower, it does not.

### unblockableMoves <a id="unblockable"></a>
#### Description
Returns an integer denoting which player has more valid moves that cannot be easily blocked due to an "open" sequence. This is achieved by simply subtracting openSequences from openMoves. If the integer is positive, then player one has more "un-blockable" moves. If the integer is negative, then player two has more. The term "blockable" here is very specific, referring only to sequences which can be blocked by inserting a tile somewhere in the middle of it.

#### Strategy
This feature was chosen to determine whether moves that could be easily completed/blocked by placing checkers in the center of them perform better or worse than moves which can only be completed/blocked by placing checkers on either end.

# Training With Features

## Features as a Decision Tree
### WEKA procedures
### Cross validation performance

## Neural Network
### WEKA procedures
### Cross Validation

  Cross validation is way to estimate the sample error rate of data models. This is done by breaking example data into both training sets and testing sets (also known as *validation sets*).

  Cross-validation helps prevent **overfitting**, a phenomenon where random noise (errors) overpower the actual data of the model, resulting in poor predictive performance.

  The second goal is to making sure our model will **generalize well** on future predictions. Cross validation helps us to select the best model among our hypothesis space by calculating average validation error rate and filtering out the one minimizing them.

## What cross validation we performed?
We choose k-fold cross validation algorithm as default. Compared with holdout cross validation, k-fold algorithm ensures maximize data utilization. It spilt data into k equal subset and performs k round of train meaning while holding out 1 of data set out as test set and taking remaining data as training data sets. Holding out cross validation holds part of data out as training set, failing to utilize available data, and leads to poor hypothesis.

# Result
### How did we figure out which feature is important?

### What did we find?

### How accurate our experiments are?
