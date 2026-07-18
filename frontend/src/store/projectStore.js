import create from 'zustand';

const useProjectStore = create((set, get) => ({
  projects: [],
  currentProject: null,
  loading: false,
  error: null,

  fetchProjects: async (token) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch('http://localhost:5000/api/projects', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!response.ok) throw new Error('Failed to fetch projects');
      
      const data = await response.json();
      set({ projects: data.projects, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  fetchProject: async (id, token) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch(`http://localhost:5000/api/projects/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!response.ok) throw new Error('Failed to fetch project');
      
      const data = await response.json();
      set({ currentProject: data, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },

  generateProject: async (formData, token) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) throw new Error('Generation failed');
      
      const data = await response.json();
      set({ loading: false });
      return data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  deleteProject: async (id, token) => {
    try {
      const response = await fetch(`http://localhost:5000/api/projects/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!response.ok) throw new Error('Failed to delete project');
      
      set(state => ({
        projects: state.projects.filter(p => p.id !== id)
      }));
    } catch (error) {
      set({ error: error.message });
    }
  }
}));

export { useProjectStore };
