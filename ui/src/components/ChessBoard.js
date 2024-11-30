import "./ChessBoard.css";
import { useState } from "react";
import axios from "axios";
import Chess from "chess.js";
import { Chessboard } from "react-chessboard";
import Constants from "../constants";

export default function ChessBoard() {
  const [game, setGame] = useState(new Chess());
  const [isLoading, setIsLoading] = useState(false); // Loading state

  function safeGameMutate(modify) {
    setGame((g) => {
      const update = Object.assign(Object.create(Object.getPrototypeOf(g)), g);
      modify(update);
      return update;
    });
  }

  async function makeEngineMove(moves) {
    if (game.game_over() || game.in_draw()) return;

    setIsLoading(true); // Start loading state

    let response;
    let url = Constants.backend_url + "/predict";
    let parsedMoves = moves.replace(new RegExp(/\d+\. /, "g"), "");
    console.log(parsedMoves);

    try {
      const res = await axios.post(url, { input_moves: parsedMoves });
      response = res.data.moves;
      console.log(res.data);
    } catch (error) {
      console.error("Engine move error:", error);
      response = {
        success: false,
        object: error.response && error.response.data,
      };
    } finally {
      setIsLoading(false); // End loading state
    }

    safeGameMutate((game) => {
      game.load_pgn(response);
    });
  }

  function onDrop(sourceSquare, targetSquare) {
    let move = null;

    safeGameMutate((game) => {
      move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: "q", // always promote to a queen for simplicity
      });
    });

    if (move === null) return false; // illegal move

    makeEngineMove(game.pgn());

    return true;
  }

  function undoLastMove() {
    safeGameMutate((game) => {
      game.undo();
      game.undo(); // Undo both player and engine moves
    });
  }

  function resetBoard() {
    safeGameMutate((game) => {
      game.reset();
    });
  }

  return (
    <div className="board-panel">
      <div>
        <Chessboard
          position={game.fen()}
          onPieceDrop={onDrop}
          boardWidth={500} // Adjust size as needed
        />
        {isLoading && <p className="loading-text">Calculating move...</p>}
      </div>
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
