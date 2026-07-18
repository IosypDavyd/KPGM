import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

const Dashboard = () => {
  const { token } = useAuthStore();

  return (
    <div className="container">
      {/* Hero Section */}
      <section className="py-20 text-center">
        <h1 className="text-5xl font-bold mb-6 gradient-text">
          KPGM Music Video Generator
        </h1>
        <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
          Створюйте професійні музичні кліпи за допомогою штучного інтелекту.
          Просто опишіть музику - ми створимо видео!
        </p>
        {token ? (
          <Link to="/generator" className="btn btn-primary text-lg px-8 py-3">
            Почати генерацію
          </Link>
        ) : (
          <Link to="/register" className="btn btn-primary text-lg px-8 py-3">
            Розпочати безкоштовно
          </Link>
        )}
      </section>

      {/* Features Section */}
      <section className="py-20 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="card text-center">
          <div className="text-4xl mb-4">🎵</div>
          <h3 className="text-xl font-bold mb-3">SUNO AI Музика</h3>
          <p className="text-gray-400">Генеруйте унікальну музику з текстового опису</p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">🎬</div>
          <h3 className="text-xl font-bold mb-3">Генерація Відео</h3>
          <p className="text-gray-400">Автоматично створюйте синхронізовані відеокліпи</p>
        </div>
        <div className="card text-center">
          <div className="text-4xl mb-4">⚡</div>
          <h3 className="text-xl font-bold mb-3">Швидка обробка</h3>
          <p className="text-gray-400">Отримуйте результати за лічені хвилини</p>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
