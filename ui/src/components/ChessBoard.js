import "./ChessBoard.css";
import { useState, useEffect } from "react";
import axios from "axios";
import Chess from "chess.js";
import { Chessboard } from "react-chessboard";
import Constants from "../constants";
import HexGridBackground from "./HexGridBackground";

export default function ChessBoard() {
  const [game, setGame] = useState(new Chess());
  const [isLoading, setIsLoading] = useState(false);
  const [winner, setWinner] = useState(null);

  function safeGameMutate(modify) {
    setGame((g) => {
      const update = Object.assign(Object.create(Object.getPrototypeOf(g)), g);
      modify(update);
      return update;
    });
  }

  function checkGameOver() {
    if (game.in_checkmate()) {
      const winnerColor = game.turn() === "w" ? "Black" : "White";
      setWinner(`${winnerColor} Wins!`);
    }
  }

  async function makeEngineMove(moves) {
    if (game.game_over() || game.in_draw()) return;

    setIsLoading(true);

    let response;
    let url = Constants.backend_url + "/predict";
    let parsedMoves = moves.replace(new RegExp(/\d+\. /, "g"), "");

    try {
      const res = await axios.post(url, { input_moves: parsedMoves });
      response = res.data.moves;
    } catch (error) {
      console.error("Engine move error:", error);
      response = {
        success: false,
        object: error.response && error.response.data,
      };
    } finally {
      setIsLoading(false);
    }

    safeGameMutate((game) => {
      game.load_pgn(response);
    });

    checkGameOver();
  }

  function onDrop(sourceSquare, targetSquare) {
    let move = null;

    safeGameMutate((game) => {
      move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: "q",
      });
    });

    if (move === null) return false;

    makeEngineMove(game.pgn());

    checkGameOver();

    return true;
  }

  function undoLastMove() {
    setWinner(null);
    safeGameMutate((game) => {
      game.undo();
      game.undo();
    });
  }

  function resetBoard() {
    setWinner(null);
    safeGameMutate((game) => {
      game.reset();
    });
  }

  return (
    <div className="board-panel">
      {/* Add hexagonal grid background */}
      <HexGridBackground isThinking={isLoading} />

      {/* Chessboard */}
      <div>
        <Chessboard position={game.fen()} onPieceDrop={onDrop} boardWidth={500} />
        {isLoading && <p className="loading-text">Calculating move...</p>}
        {winner && <p className="winner-text">{winner}</p>}
      </div>

      {/* Moves Box & Buttons (Now aligned to the right) */}
      <div className="board-information">
        <div className="board-moves">
          <p>{game.pgn()}</p>
        </div>
        <div className="mt-8">
          <button className="button button-warning mh-8" onClick={undoLastMove}>
            Undo
          </button>
          <button className="button button-warning mh-8" onClick={resetBoard}>
            Reset
          </button>
        </div>
      </div>
    </div>
  );
}
