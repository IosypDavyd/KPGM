import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Generator from './pages/Generator';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import { useAuthStore } from './store/authStore';
import { Toaster } from 'react-hot-toast';

function App() {
  const { token, checkAuth } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
    setLoading(false);
  }, [checkAuth]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="loading"></div>
      </div>
    );
  }

  return (
    <Router>
      <Toaster position="top-right" />
      <Navbar />
      <main className="min-h-screen pt-16">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={!token ? <Login /> : <Navigate to="/" />} />
          <Route path="/register" element={!token ? <Register /> : <Navigate to="/" />} />
          <Route path="/generator" element={token ? <Generator /> : <Navigate to="/login" />} />
          <Route path="/projects" element={token ? <Projects /> : <Navigate to="/login" />} />
          <Route path="/projects/:id" element={token ? <ProjectDetail /> : <Navigate to="/login" />} />
        </Routes>
      </main>
      <Footer />
    </Router>
  );
}

export default App;
