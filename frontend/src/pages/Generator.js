import React, { useState } from 'react';
import { useAuthStore } from '../store/authStore';
import { useProjectStore } from '../store/projectStore';
import toast from 'react-hot-toast';

const Generator = () => {
  const { token } = useAuthStore();
  const { generateProject, loading } = useProjectStore();
  const [formData, setFormData] = useState({
    text: '',
    style: 'ambient',
    duration: 60,
    video: true,
    video_style: 'cinematic',
    project_name: ''
  });
  const [generatedProject, setGeneratedProject] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await generateProject(formData, token);
      setGeneratedProject(result);
      toast.success('Генерація розпочата!');
    } catch (error) {
      toast.error(error.message);
    }
  };

  return (
    <div className="container py-10">
      <h1 className="text-4xl font-bold mb-10 gradient-text">Генератор Музики та Відео</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form */}
        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">Назва проекту</label>
              <input
                type="text"
                name="project_name"
                value={formData.project_name}
                onChange={handleChange}
                placeholder="Мій музичний клип"
                className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Опис музики *</label>
              <textarea
                name="text"
                value={formData.text}
                onChange={handleChange}
                placeholder="Опишіть музику, яку ви хочете створити..."
                rows="4"
                required
                className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Жанр</label>
                <select
                  name="style"
                  value={formData.style}
                  onChange={handleChange}
                  className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
                >
                  <option value="ambient">Ambient</option>
                  <option value="electronic">Electronic</option>
                  <option value="pop">Pop</option>
                  <option value="rock">Rock</option>
                  <option value="hip-hop">Hip-Hop</option>
                  <option value="jazz">Jazz</option>
                  <option value="classical">Classical</option>
                  <option value="indie">Indie</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Тривалість (сек)</label>
                <input
                  type="number"
                  name="duration"
                  value={formData.duration}
                  onChange={handleChange}
                  min="30"
                  max="300"
                  className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
                />
              </div>
            </div>

            <div className="flex items-center">
              <input
                type="checkbox"
                name="video"
                checked={formData.video}
                onChange={handleChange}
                className="w-4 h-4 rounded"
              />
              <label className="ml-3">Генерувати відео</label>
            </div>

            {formData.video && (
              <div>
                <label className="block text-sm font-medium mb-2">Стиль відео</label>
                <select
                  name="video_style"
                  value={formData.video_style}
                  onChange={handleChange}
                  className="w-full bg-black/30 border border-purple-500/30 rounded-lg px-4 py-2 focus:outline-none focus:border-purple-500"
                >
                  <option value="cinematic">Cinematic</option>
                  <option value="abstract">Abstract</option>
                  <option value="nature">Nature</option>
                  <option value="urban">Urban</option>
                  <option value="psychedelic">Psychedelic</option>
                  <option value="minimalist">Minimalist</option>
                </select>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full btn btn-primary py-3"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <span className="loading"></span> Генерація...
                </span>
              ) : (
                '🚀 Генерувати'
              )}
            </button>
          </form>
        </div>

        {/* Preview */}
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Попередній перегляд</h2>
          {generatedProject ? (
            <div className="space-y-4">
              <div className="bg-black/50 p-4 rounded-lg">
                <p className="text-sm text-gray-400 mb-2">Статус</p>
                <p className="font-semibold text-green-400">{generatedProject.status}</p>
              </div>
              <div className="bg-black/50 p-4 rounded-lg">
                <p className="text-sm text-gray-400 mb-2">ID Проекту</p>
                <p className="font-mono text-sm">{generatedProject.project_id}</p>
              </div>
              <div className="bg-black/50 p-4 rounded-lg">
                <p className="text-sm text-gray-400 mb-2">Прогрес</p>
                <div className="w-full bg-black/50 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all"
                    style={{ width: `${generatedProject.progress}%` }}
                  ></div>
                </div>
                <p className="text-sm mt-2">{generatedProject.progress}%</p>
              </div>
            </div>
          ) : (
            <div className="text-center text-gray-400">
              <p className="text-6xl mb-4">🎬</p>
              <p>Заповніть форму та натисніть "Генерувати"</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Generator;
