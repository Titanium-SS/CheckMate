import './App.css';
import { Navbar } from './components/Navbar';
import ChessBoard from './components/ChessBoard';


function App() {
  return (
    <div className="App">
      <Navbar />
      <main>
        <section>
          <div className="centered-column">
            <div className="container">
              <ChessBoard />
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
