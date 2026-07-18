import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import toast from 'react-hot-toast';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      toast.success('Успішний вхід!');
      navigate('/');
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <div className="container flex items-center justify-center min-h-screen">
      <div className="card w-full max-w-md">
        <h1 className="text-3xl font-bold mb-6 gradient-text text-center">Вхід</h1>
        
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
            <label className="block text-sm font-medium mb-2">Пароль</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full btn btn-primary"
          >
            {loading ? <span className="loading"></span> : 'Вхід'}
          </button>
        </form>
        
        <p className="text-center text-gray-400 mt-4">
          Немаєте акаунту? <Link to="/register" className="text-purple-400">Зареєструйтеся</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
