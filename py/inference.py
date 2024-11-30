"""
Script for playing chess against the ChessMate engine.
The human player always plays as white.
"""

import argparse
import torch
from chessutils.configuration import get_configuration
from chessutils.model import Transformer
from chessutils.tokenizer import Tokenizer
import os
import re
import sys
from contextlib import contextmanager


@contextmanager
def suppress_output():
    """
    Context manager to suppress stdout and stderr.
    """
    with open(os.devnull, "w") as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = devnull, devnull
        try:
            yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr


def _parse_args():
    """
    Parse command-line arguments for model configuration, tokenizer, and logging.
    """
    parser = argparse.ArgumentParser(description='CheckMate inference parser')

    parser.add_argument('--load_model', type=str, default="model/checkmate.pth",
                        help='Path to the model for inference')
    parser.add_argument('--config', type=str, default="configs/default.yaml",
                        help='Path to the configuration file (YAML format)')
    parser.add_argument('--tokenizer', type=str, default="vocab/vocab.txt",
                        help='Path to the tokenizer vocabulary file')
    parser.add_argument('--log_file', type=str, default="game_log.txt",
                        help='File to log moves of the game')

    return parser.parse_args()


def log_move(log_file, move):
    """
    Logs each move to a specified file.

    Args:
        log_file (str): Path to the log file.
        move (str): Chess move to log.
    """
    with open(log_file, "a") as file:
        file.write(f"{move}\n")


def is_valid_move(move):
    """
    Basic validation for chess move notation in PGN format.

    Args:
        move (str): Move in PGN format.

    Returns:
        bool: True if move is in valid PGN format, False otherwise.
    """
    # Pattern includes typical moves and castling notation
    pgn_move_pattern = re.compile(r"^(O-O|O-O-O|[KQBNR]?[a-h]?[1-8]?[x-]?[a-h][1-8])$")
    return bool(pgn_move_pattern.match(move))


def main(args) -> None:
    """
    Main function to run the chess game between the human player and engine.

    Args:
        args (Namespace): Parsed command-line arguments.
    """
    with suppress_output():
        # Load configuration and tokenizer for the model
        config = get_configuration(args.config)
        tokenizer = Tokenizer(args.tokenizer)

        # Initialize model and set device (GPU if available, otherwise CPU)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = Transformer(
            tokenizer=tokenizer,
            num_tokens=tokenizer.vocab_size(),
            dim_model=config["model"]["dim_model"],
            d_hid=config["model"]["d_hid"],
            num_heads=config["model"]["num_heads"],
            num_layers=config["model"]["num_layers"],
            dropout_p=config["model"]["dropout_p"],
            n_positions=config["model"]["n_positions"],
        )
        try:
            model.load_state_dict(torch.load(args.load_model, map_location=device))
            model.eval()  # Set model to evaluation mode
            model.to(device)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            return

    # Prepare game log and initial instructions
    if os.path.exists(args.log_file):
        os.remove(args.log_file)  # Clear previous log

    print(
        "===== CheckMate Engine =====\n"
        "    Enter valid moves in PGN format.\n"
        "    Enter \\b to undo a move.\n"
        "    Enter \\m to show all moves\n"
    )

    input_string = "<bos>"  # Start of game token
    boards = [input_string]  # Stack to store game states

    # Main game loop
    while (len(input_string.split(" ")) < config["model"]["n_positions"]
           and input_string.split(" ")[-1] != tokenizer.eos_token):
        
        next_move = input("WHITE MOVE: ")

        if next_move == "\\m":
            print("Moves so far:", input_string)
            continue
        elif next_move == "\\b":
            if len(boards) > 1:
                boards.pop()
            input_string = boards[-1]
            continue

        # Check for a valid move format
        if not is_valid_move(next_move):
            print("ILLEGAL MOVE FORMAT. Please, try again.")
            continue

        # Store previous state in case of invalid engine response
        prev_input_string = input_string
        input_string += " " + next_move

        # Log human's move
        log_move(args.log_file, f"White: {next_move}")

        try:
            # Engine predicts next move for black
            with suppress_output():
                input_string = model.predict(
                    input_string,
                    stop_at_next_move=True,
                    temperature=0.2,
                )
            boards.append(input_string)
            black_move = input_string.split(" ")[-1]
            print("BLACK MOVE:", black_move)

            # Log engine's move
            log_move(args.log_file, f"Black: {black_move}")

        except ValueError:
            input_string = prev_input_string  # Rollback state on invalid move
            print("ILLEGAL MOVE. Please, try again.")
        except Exception as e:
            print(f"UNHANDLED EXCEPTION: {e}")

    print("--- Final board ---")
    print(input_string)


if __name__ == "__main__":
    args = _parse_args()
    main(args)
