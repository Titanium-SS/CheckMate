"""
Flask API for interacting with the CheckMate engine.
This server provides an endpoint to predict the next move given the sequence of moves played.
"""

import argparse
import torch
from chessutils.configuration import get_configuration
from chessutils.model import Transformer
from chessutils.tokenizer import Tokenizer
from flask import Flask, request, jsonify, make_response
import os

def _parse_args():
    """
    Parse command-line arguments to configure model, tokenizer, and configuration paths.
    """
    parser = argparse.ArgumentParser(description='CheckMate inference parser')

    parser.add_argument('--load_model', type=str, default="model/checkmate.pth",
                        help='Path to the model for inference')
    parser.add_argument('--config', type=str, default="configs/default.yaml",
                        help='Path to the configuration file (YAML format)')
    parser.add_argument('--tokenizer', type=str, default="vocab/vocab.txt",
                        help='Path to the tokenizer vocabulary file')

    return parser.parse_args()

# Initialize Flask app and CORS headers configuration
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

# Parse arguments and load configuration, tokenizer, and model
args = _parse_args()
config = get_configuration(args.config)
tokenizer = Tokenizer(args.tokenizer)

# Configure device for model inference (GPU if available, else CPU)
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

# Load model weights onto the appropriate device
try:
    print("Loading model...")
    model.load_state_dict(torch.load(args.load_model, map_location=device))
    model.to(device)
    model.eval()  # Set model to evaluation mode
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")

def _build_cors_preflight_response():
    """
    Build a preflight CORS response for OPTIONS requests.
    """
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    """
    Add CORS headers to an actual response.
    """
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Endpoint to predict the next move in a chess game.
    Accepts a JSON request with 'input_moves' (PGN string of moves played so far).
    """
    if request.method == "OPTIONS":  # Handle CORS preflight request
        return _build_cors_preflight_response()
    elif request.method == 'POST':
        request_data = request.get_json()

        # Validate input data
        if request_data is None or 'input_moves' not in request_data:
            response = {'success': False, 'message': 'Bad request'}
            return _corsify_actual_response(jsonify(response))

        # Prepare input moves for model prediction
        input_moves = tokenizer.bos_token + " " + request_data['input_moves'].strip()

        try:
            # Perform inference without gradient computation to save memory
            with torch.no_grad():
                output_moves = model.predict(
                    input_moves,
                    stop_at_next_move=True,
                    temperature=0.2,
                )
        except ValueError:
            # Handle illegal moves gracefully
            response = {'success': False, 'message': "Illegal move."}
            return _corsify_actual_response(jsonify(response))
        except Exception as e:
            print(f"Error: {e}")
            response = {'success': False, 'message': "Unhandled error."}
            return _corsify_actual_response(jsonify(response))

        # Process and format the output
        output_moves = output_moves.replace("<bos> ", "")
        response = {'success': True, 'moves': output_moves}
        return _corsify_actual_response(jsonify(response))

if __name__ == '__main__':
    app.run(threaded=True)
