import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { useProjectStore } from '../store/projectStore';

const Projects = () => {
  const { token } = useAuthStore();
  const { projects, loading, fetchProjects } = useProjectStore();

  useEffect(() => {
    if (token) {
      fetchProjects(token);
    }
  }, [token, fetchProjects]);

  return (
    <div className="container py-10">
      <h1 className="text-4xl font-bold mb-10 gradient-text">Мої проекти</h1>

      {loading ? (
        <div className="flex justify-center">
          <div className="loading"></div>
        </div>
      ) : projects.length === 0 ? (
        <div className="card text-center py-10">
          <p className="text-gray-400 mb-4">Немає проектів</p>
          <Link to="/generator" className="btn btn-primary">
            Створити перший проект
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map(project => (
            <Link key={project.id} to={`/projects/${project.id}`}>
              <div className="card cursor-pointer hover:border-purple-400 transition">
                <h3 className="text-lg font-bold mb-2">{project.name}</h3>
                <p className="text-sm text-gray-400 mb-4">
                  {new Date(project.created_at).toLocaleDateString('uk-UA')}
                </p>
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-2 py-1 rounded ${
                    project.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                    project.status === 'processing' ? 'bg-blue-500/20 text-blue-400' :
                    'bg-gray-500/20 text-gray-400'
                  }`}>
                    {project.status}
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default Projects;
