javascript
import { Link, useNavigate } from 'react-router-dom';

function Header() {
  const navigate = useNavigate();
  const token = localStorage.getItem('token');
  const isAdmin = localStorage.getItem('isAdmin') === 'true';

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('isAdmin');
    navigate('/login');
  };

  return (
    <nav className="bg-blue-600 p-4 text-white">
      <div className="container mx-auto flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold">Shopt1</Link>
        <div>
          {token ? (
            <>
              <Link to="/dashboard" className="mr-4">Tài Khoản</Link>
              {isAdmin && <Link to="/admin" className="mr-4">Admin</Link>}
              <button onClick={handleLogout} className="bg-red-500 px-4 py-2 rounded">Đăng Xuất</button>
            </>
          ) : (
            <>
              <Link to="/login" className="mr-4">Đăng Nhập</Link>
              <Link to="/register">Đăng Ký</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Header;
