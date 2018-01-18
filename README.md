# IdealPlacement_ROI

# Generate a Region of Interest (ROI) for the highest scoring zoid orientation and location as determined by CERL models.

The all_analysis.py and translate_test.py must be placed under the Tetris-AI repo when downloaded in order to use some of the
functions defined in those files.

Running the all_analysis program will prompt the user for a file containing data from a singular game. (Do not forget .tsv extension)
The analysis program will create and write to 4 files:


1) [game_data_file]_predictions

		Gives possible moves to be made per episode, data is formatted with the header:
		
		episode_number	zoid	move_row	move_col	move_rot	move_score


2) [game_data_file]_analysis

		From all possible moves per episode (as given in the _predictions file), this file will tell you 
		whether the move actually made was an option in _predictions, and if so, its rank (# points it achieves
			compared to the other options). Data is formatted with header:

		episode_number	zoid	move_row	move_col	move_rot	move_score	move_rank	num_options


3) [game_data_file]_best_moves_byep

		From all possible moves per episode (as given in the _predictions file), this file will find the 
		highest scoring move per episode, output it and the zoid representation. Data is formatted with header:

		zoid	move_row	move_col	move_rot	move_score	zoid_rep


4) [game_data_file]_zoid_reps

		From the _best_moves_byep file, the ideal zoid placement will be taken and used to create a file of only the zoid
		representations on the Tetris board. This will then be used to define the ROI within the game for every episode.
