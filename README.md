# CHECKMATE
<hr> <div align="center"> <img src="readme/logo.png" height=300> <p><b>AI-Powered Chess with a Stunning UI</b></p> </div> <hr>

## 🚀 Tech Stack
### Backend:
<div align="center"> <a href="https://www.python.org/" target="_blank"> <img src="readme/python.png" height=70> </a> </div>

### Frontend:
<div align="center"> <a href="https://react.dev/" target="_blank"> <img src="readme/react-js.png" height=70> </a> </div>

### Libraries Used:
<div align="center"> <a href="https://pytorch.org/" target="_blank"> <img src="readme/pytorch.png" height=70> </a> <a href="https://flask.palletsprojects.com/" target="_blank"> <img src="readme/flask.png" height=70> </a> <a href="https://axios-http.com/" target="_blank"> <img src="readme/axiosjs.webp" height=30> </a> </div> <hr>

## 🎯 About
Checkmate is an AI-powered chess application that brings intelligent gameplay and a modern, futuristic UI to the table.

### 🔥 New Features:
✅ Hexagonal Circuit-Themed Background that glows dynamically when the AI is thinking.
✅ Refined UI Design with centered layout and better move tracking panel.
✅ Improved Interactions with enhanced animations, responsiveness, and user experience.

This project demonstrates the power of AI in chess while providing an engaging and visually appealing interface.

<hr>

### 📂 File Structure

```plaintext
checkmate/
│
├── py/                        # Backend Python project
│   ├── model/                 # Trained Transformer models and checkpoints
│   ├── dataset/               # Dataset used in training the model
│   ├── vocab/                 # Contains unique chess moves
│   ├── chessutils/            # Chess-specific utility scripts
│   ├── play.py                # Flask server for the backend
│   ├── requirements.txt       # Python dependencies
│   └── ...                    # Other backend scripts
│
├── ui/                        # Frontend React project
│   ├── src/                   # React source files
│   ├── public/                # Static assets for the React app
│   ├── package.json           # Node.js dependencies
│   └── ...                    # Other frontend files
│
├── readme/                    # README-related images
│
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
└── ...
```
<hr>

### 🏗️ Train Your Own Model
Want to train a custom chess AI? Follow these steps:

1️⃣ Download the dataset from Kaggle: <a href="https://www.kaggle.com/milesh1/35-million-chess-games">35 Million Chess Games</a> [currently under review] <a href="https://www.kaggle.com/datasets/liury123/chess-game-from-12-top-players">Alternative</a>
2️⃣ Rename it to `original_data.txt` and place it in the `data/` folder.
3️⃣ Run `process_data.`py` to automatically generate a vocabulary file.
4️⃣ Train the model using:

```bash
python train.py
```
5️⃣ The trained model will be saved in the `model/` directory.

<hr>

### 🕹️ How to Use

1️⃣ Clone the repository

```bash
git clone https://github.com/Titanium-SS/checkmate.git
cd checkmate
```

2️⃣ Set Up the Backend (Python)
```bash
cd py
pip install -r requirements.txt
python play.py
```

3️⃣ Set Up the Frontend (React)
```bash
cd ui
npm install
npm start
```
4️⃣ Open Your Browser
Go to: http://localhost:3000 and start playing!

<hr>

### 🎮 Gameplay
<div align="center"> <img src="readme/ui_1.png" height=300> <img src="readme/ui_2.png" height=300> </div>

<hr>

### New UI Highlights:
✅ Chessboard centered with an enhanced move tracking panel
✅ Undo and Reset buttons neatly aligned
✅ Futuristic hexagonal circuit-themed background

<hr>

### ✨ Features
✔ **AI-powered move prediction** – Uses a Transformer model for intelligent gameplay.
✔ **Dynamic background glow effect** – Only activates when the AI is thinking.
✔ **Refined and Responsive UI** – Sleek animations, modern buttons, and a clean layout.
✔ **Move History Panel** – Displays all previous moves with smooth scrolling.
✔ **Undo & Reset functionality** – Instant game reset or undo your last move.
✔ **Seamless Backend Integration** – Flask-based API serves AI-generated moves efficiently.

<hr>

### 🚀 Future Enhancements
**🔹 Cloud Deployment** – Play chess online with real-time AI computation.
**🔹 Stronger AI Model** – Improve move predictions using reinforcement learning.
**🔹 Dark Mode** – Add a toggle between light and dark themes.
**🔹 Multiplayer Mode** – Play against other human players with AI assistance.
**🔹 Mobile App** - Make a Mobile compatible Web App.

<hr>

### 🏆 Contributors
👨‍💻 Shailendra Singh – Developer & Maintainer 🚀
📌 GitHub: <a href="https://github.com/Titanium-SS">Titanium-SS</a>

## 🌟 Enjoy playing AI Chess with CheckMate! ♟️🔥