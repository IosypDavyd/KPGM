import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useProjectStore } from '../store/projectStore';

const ProjectDetail = () => {
  const { id } = useParams();
  const { token } = useAuthStore();
  const { currentProject, loading, fetchProject } = useProjectStore();

  useEffect(() => {
    if (token && id) {
      fetchProject(id, token);
    }
  }, [token, id, fetchProject]);

  if (loading) {
    return (
      <div className="container py-10 flex justify-center">
        <div className="loading"></div>
      </div>
    );
  }

  if (!currentProject) {
    return (
      <div className="container py-10">
        <p className="text-gray-400">Проект не знайдено</p>
      </div>
    );
  }

  return (
    <div className="container py-10">
      <h1 className="text-4xl font-bold mb-8 gradient-text">{currentProject.name}</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          {currentProject.video_url && (
            <div className="card mb-6">
              <h2 className="text-2xl font-bold mb-4">Відео</h2>
              <video controls className="w-full rounded-lg">
                <source src={currentProject.video_url} type="video/mp4" />
                Ваш браузер не підтримує відеотег.
              </video>
            </div>
          )}

          {currentProject.music_url && (
            <div className="card">
              <h2 className="text-2xl font-bold mb-4">Музика</h2>
              <audio controls className="w-full">
                <source src={currentProject.music_url} type="audio/mpeg" />
                Ваш браузер не підтримує аудіотег.
              </audio>
            </div>
          )}
        </div>

        <div>
          <div className="card space-y-4">
            <div>
              <p className="text-sm text-gray-400">Статус</p>
              <p className="font-semibold">{currentProject.status}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Прогрес</p>
              <div className="w-full bg-black/50 rounded-full h-2 mt-2">
                <div
                  className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                  style={{ width: `${currentProject.progress}%` }}
                ></div>
              </div>
              <p className="text-sm mt-2">{currentProject.progress}%</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Жанр</p>
              <p className="font-semibold">{currentProject.music_style}</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Тривалість</p>
              <p className="font-semibold">{currentProject.duration} сек</p>
            </div>
            <div>
              <p className="text-sm text-gray-400">Створено</p>
              <p className="font-semibold">{new Date(currentProject.created_at).toLocaleString('uk-UA')}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetail;
