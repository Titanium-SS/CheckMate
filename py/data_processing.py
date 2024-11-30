"""
Script to process a Kaggle dataset containing chess games, extract individual matches,
and create a vocabulary of unique chess moves. The script processes raw data,
cleans and filters it, and then saves both the cleaned games and the vocabulary
to separate files.

Dataset used: https://www.kaggle.com/milesh1/35-million-chess-games
"""

import os
import re

if __name__ == "__main__":
    # Set to store unique chess moves for vocabulary creation
    vocab_counter = set()

    # Open output file to save processed games
    with open("dataset/processed_data.txt", "w", encoding="utf-8") as outf:
        # Open the raw input file containing chess games
        with open("dataset/original_data.txt", "r", encoding="utf-8") as inpf:
            for line in inpf:
                try:
                    # Extract moves from each line after the "###" delimiter
                    ostr = line.split("###")[1].strip()
                    
                    # Remove move labels like "W1.", "B2.", which denote turn numbers
                    ostr = re.sub(r"W\d+\.", "", ostr)  # Remove white move indicators
                    ostr = re.sub(r"B\d+\.", "", ostr)  # Remove black move indicators

                    # If the line contains valid moves, process further
                    if len(ostr) > 0:
                        # Ensure each move sequence ends with a newline
                        if ostr[-1] != '\n':
                            ostr += '\n'

                        # Write cleaned move sequence to output file
                        outf.write(ostr)

                        # Split moves by space and add them to the vocabulary set
                        for move in ostr.split(" "):
                            move = move.replace("\n", "")
                            if move != "":
                                vocab_counter.add(move)  # Add unique move to vocabulary
                    else:
                        # Placeholder if line is empty or contains no moves
                        pass
                except:
                    # Skip lines that don't match expected format
                    pass

        # Create directory to store vocabulary file if it doesn't exist
        os.makedirs("vocab", exist_ok=True)

        # Write unique vocabulary moves to a separate file
        with open("vocab/vocab.txt", "w", encoding="utf-8") as f:
            for v in vocab_counter:
                f.write(v + "\n")
