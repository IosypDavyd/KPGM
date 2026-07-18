import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import toast from 'react-hot-toast';

const Register = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const { register, loading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      toast.error('Паролі не збігаються');
      return;
    }

    try {
      await register(email, username, password);
      toast.success('Успішна реєстрація! Тепер увійдіть.');
      navigate('/login');
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <div className="container flex items-center justify-center min-h-screen">
      <div className="card w-full max-w-md">
        <h1 className="text-3xl font-bold mb-6 gradient-text text-center">Реєстрація</h1>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Ім'я користувача</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Пароль</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Підтвердіть пароль</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full btn btn-primary"
          >
            {loading ? <span className="loading"></span> : 'Реєстрація'}
          </button>
        </form>
        
        <p className="text-center text-gray-400 mt-4">
          Вже маєте акаунт? <Link to="/login" className="text-purple-400">Увійдіть</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
