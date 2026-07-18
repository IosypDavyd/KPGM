import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const Navbar = () => {
  const { token, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="fixed top-0 left-0 right-0 bg-gradient-to-r from-[#0f0f1e] to-[#1a1a2e] border-b border-purple-500/20 z-50">
      <div className="container flex items-center justify-between h-16">
        <Link to="/" className="flex items-center gap-2">
          <div className="text-2xl font-bold gradient-text">🎵 KPGM</div>
          <span className="text-sm text-purple-400">Music Video Generator</span>
        </Link>

        <div className="flex items-center gap-6">
          {token ? (
            <>
              <Link to="/generator" className="hover:text-purple-400 transition">
                Генератор
              </Link>
              <Link to="/projects" className="hover:text-purple-400 transition">
                Проекти
              </Link>
              <button
                onClick={handleLogout}
                className="btn btn-primary"
              >
                Вихід
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="hover:text-purple-400 transition">
                Вхід
              </Link>
              <Link to="/register" className="btn btn-primary">
                Реєстрація
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
