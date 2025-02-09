import * as React from "react";
import "./Navbar.css";

export const Navbar = () => {
  React.useEffect(() => {
    const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890";
    const logoText = document.querySelector(".logo-text");
    let interval = null;

    if (logoText) {
      logoText.onmouseover = (event) => {
        let iteration = 0;
        clearInterval(interval);

        interval = setInterval(() => {
          event.target.innerText = event.target.innerText
            .split("")
            .map((letter, index) =>
              index < iteration ? event.target.dataset.value[index] : letters[Math.floor(Math.random() * letters.length)]
            )
            .join("");

          if (iteration >= event.target.dataset.value.length) {
            clearInterval(interval);
          }

          iteration += 1 / 3;
        }, 30);
      };
    }
  }, []);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="logo">
          <img src="/logo192.png" alt="CheckMate" className="logo-image" />
          <span className="logo-text" data-value="CheckMate">
            CheckMate
          </span>
        </div>
        <div className="nav-navigation">
          <a className="button nav-button" href="https://github.com/Titanium-SS/checkmate">
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
};
