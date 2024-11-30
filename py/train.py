"""
Script for training the Transformer model on chess game data.
It defines a Trainer class to handle training and evaluation loops and uses a
transformer model for move prediction.
"""

import os
import argparse
from tqdm import tqdm
import numpy as np
import torch
from torch.utils.data import DataLoader, random_split

from chessutils.configuration import get_configuration
from chessutils.dataset import PGNDataset
from chessutils.model import Transformer
from chessutils.tokenizer import Tokenizer

def _parse_args():
    """
    Parse command-line arguments for training configurations, model paths, and hyperparameters.
    """
    parser = argparse.ArgumentParser(description='CheckMate training parser')

    parser.add_argument('--config', type=str, default="configs/default.yaml",
                        help='Path to the configuration file (YAML format)')
    parser.add_argument('--tokenizer', type=str, default="vocab/vocab.txt",
                        help='Path to the tokenizer vocabulary file')
    parser.add_argument('--dataset', type=str, default="dataset/processed_data.txt",
                        help='Path to the processed dataset')
    parser.add_argument('--vocab', type=str, default='./vocab/vocab.txt',
                        help='Path to the vocabulary file')
    parser.add_argument('--batch_size', type=int, default=64,
                        help='Training batch size')
    parser.add_argument('--epochs', type=int, default=25,
                        help='Number of training epochs')
    parser.add_argument('--lr', type=float, default=0.00025,
                        help='Learning rate')
    parser.add_argument('--beta1', type=float, default=0.9,
                        help='Adam optimizer beta1 parameter')
    parser.add_argument('--save_dir', type=str, default='./model',
                        help='Directory to save the trained model')
    parser.add_argument('--load_model', type=str, default=None,
                        help='Path to a pre-trained model for resuming training')

    return parser.parse_args()

class Trainer:
    """
    Trainer class for handling model training and evaluation.
    """
    def __init__(self, model, train_loader, val_loader, loss_fn, save_dir="./model",
                 learning_rate=0.001, num_epochs=10, adam_beta=0.5):
        self.save_dir = save_dir
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.lr = learning_rate
        self.loss_fn = loss_fn
        self.num_epochs = num_epochs

        # Optimizer with specified beta parameter
        self.optimizer = torch.optim.Adam(
            self.model.parameters(), lr=self.lr, betas=(adam_beta, 0.999)
        )

        # Configure device and move model to appropriate device
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        print(f'Selected device: {self.device}.')
        self.model.to(self.device)

    def train_epoch(self) -> float:
        """
        Trains the model for one epoch and returns the average training loss.
        """
        self.model.train()
        train_loss = []

        for local_batch in tqdm(self.train_loader):
            X = local_batch.to(self.device).t().contiguous()

            # Prepare inputs and expected outputs by shifting
            y_input = X[:-1]
            y_expected = X[1:].reshape(-1)

            # Obtain masks for attention mechanism
            sequence_length = y_input.size(0)
            src_mask = self.model.get_src_mask(sequence_length).to(self.device).bool()
            pad_mask = self.model.get_pad_mask(y_input, self.model.tokenizer.pad_token_index).to(self.device).bool()

            # Model forward pass
            pred = self.model(y_input, src_mask, pad_mask)

            # Compute loss
            loss = self.loss_fn(pred.view(-1, self.model.tokenizer.vocab_size()), y_expected)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            train_loss.append(loss.detach().cpu().numpy())

        return np.mean(train_loss)

    def test_epoch(self) -> float:
        """
        Evaluates the model on the validation set and returns the average validation loss.
        """
        self.model.eval()
        total_loss = 0.0

        with torch.no_grad():
            for local_batch in self.val_loader:
                X = local_batch.to(self.device).t().contiguous()

                # Prepare inputs and expected outputs by shifting
                y_input = X[:-1]
                y_expected = X[1:].reshape(-1)

                # Obtain masks for attention mechanism
                sequence_length = y_input.size(0)
                src_mask = self.model.get_src_mask(sequence_length).to(self.device).bool()
                pad_mask = self.model.get_pad_mask(y_input, self.model.tokenizer.pad_token_index).to(self.device).bool()

                # Model forward pass
                pred = self.model(y_input, src_mask, pad_mask)

                # Compute loss
                loss = self.loss_fn(pred.view(-1, self.model.tokenizer.vocab_size()), y_expected)
                total_loss += loss.item()

            val_loss = total_loss / len(self.val_loader)

        return val_loss

    def train(self) -> None:
        """
        Trains the model for a specified number of epochs, saving the best model based on validation loss.
        """
        best_val_loss = np.Inf

        for epoch in range(self.num_epochs):
            print(f'\n\n -------- RUNNING EPOCH {epoch + 1}/{self.num_epochs} --------\n')
            train_loss = self.train_epoch()
            val_loss = self.test_epoch() if self.val_loader else train_loss

            print(f'\n EPOCH {epoch + 1}/{self.num_epochs} \t train loss {train_loss} \t val loss {val_loss}')

            # Save the model if it achieves the best validation loss
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), os.path.join(self.save_dir, f"checkmate_{epoch + 1}.pth"))

        # Save the final model
        torch.save(self.model.state_dict(), os.path.join(self.save_dir, "checkmate.pth"))

def main(args) -> None:
    """
    Main function to initialize configurations, datasets, model, and start training.
    """
    os.makedirs(args.save_dir, exist_ok=True)
    config = get_configuration(args.config)
    tokenizer = Tokenizer(args.tokenizer)

    # Load dataset and create data loaders
    data = PGNDataset(tokenizer, args.dataset, n_positions=config["model"]["n_positions"])
    train_len = int(len(data) * 0.8)
    train_data, val_data = random_split(data, [train_len, len(data) - train_len])

    train_loader = DataLoader(train_data, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=args.batch_size, shuffle=True)

    # Initialize the transformer model
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

    # Load pre-trained model if specified
    if args.load_model:
        print("Loading pre-trained model.")
        model.load_state_dict(torch.load(args.load_model))

    loss_fn = torch.nn.NLLLoss(ignore_index=tokenizer.pad_token_index)

    # Initialize and run the trainer
    trainer = Trainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        loss_fn=loss_fn,
        save_dir=args.save_dir,
        learning_rate=args.lr,
        num_epochs=args.epochs,
        adam_beta=args.beta1
    )
    trainer.train()

if __name__ == "__main__":
    args = _parse_args()
    main(args)
