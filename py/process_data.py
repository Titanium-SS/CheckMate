"""
Script to process the Kaggle chess dataset and extract matches.
It also creates a vocabulary file from the dataset.
https://www.kaggle.com/milesh1/35-million-chess-games
"""

import os
import re

if __name__ == "__main__":
    vocab_counter = set()

    # Ensure output directories exist
    os.makedirs("vocabs", exist_ok=True)
    
    with open("dataset/processed_data.txt", "w", encoding="utf-8") as outf:
        with open("dataset/original_data.txt", "r", encoding="utf-8") as inpf:
            for line in inpf:
                try:
                    move_sequence = line.split("###")[1].strip()
                    move_sequence = re.sub(r"W\d+\.", "", move_sequence)
                    move_sequence = re.sub(r"B\d+\.", "", move_sequence)

                    if move_sequence:
                        outf.write(move_sequence + '\n')

                        for move in move_sequence.split(" "):
                            move = move.strip()
                            if move:
                                vocab_counter.add(move)
                except IndexError:
                    continue  # Skip lines that do not match the expected format

    with open("vocabs/original_vocab.txt", "w", encoding="utf-8") as f:
        for move in sorted(vocab_counter):
            f.write(move + "\n")
