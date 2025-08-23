javascript
import { Link } from 'react-router-dom';

function GameCard({ game }) {
  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <img src={game.img} alt={game.name} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h2 className="text-xl font-bold">{game.name}</h2>
        <Link to={game.path} className="mt-2 inline-block bg-blue-500 text-white px-4 py-2 rounded">
          Chơi Ngay
        </Link>
      </div>
    </div>
  );
}

export default GameCard;
