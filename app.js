javascript
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import GameCard from './components/GameCard';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import AdminPanel from './components/AdminPanel';
import LuckyWheel from './components/LuckyWheel';
import CardFlip from './components/CardFlip';
import SlotMachine from './components/SlotMachine';
import './styles.css';

// Main app with routing
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/admin" element={<AdminPanel />} />
          <Route path="/game/lucky-wheel" element={<LuckyWheel />} />
          <Route path="/game/card-flip" element={<CardFlip />} />
          <Route path="/game/slot-machine" element={<SlotMachine />} />
        </Routes>
      </div>
    </Router>
  );
}

// Home page with game cards
function Home() {
  const games = [
    { name: 'Vòng Quay May Mắn', path: '/game/lucky-wheel', img: 'wheel.jpg' },
    { name: 'Lật Thẻ', path: '/game/card-flip', img: 'card.jpg' },
    { name: 'Nổ Hũ', path: '/game/slot-machine', img: 'slot.jpg' },
  ];

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-8">Chào Mừng Đến Với Shopt1</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {games.map((game) => (
          <GameCard key={game.name} game={game} />
        ))}
      </div>
    </div>
  );
}

export default App;
