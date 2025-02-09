import React from "react";
import "./HexGridBackground.css";

export default function HexGridBackground({ isThinking }) {
  return (
    <div className="hex-grid-container">
      <div className="hex-grid"></div>
      {/* Apply glow effect when AI is thinking */}
      <div className={`glow-effect ${isThinking ? "glow-active" : ""}`}></div>
    </div>
  );
}
