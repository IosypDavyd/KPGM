import create from 'zustand';
import { persist } from 'zustand/middleware';

const useAuthStore = create(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      loading: false,
      error: null,

      login: async (email, password) => {
        set({ loading: true, error: null });
        try {
          const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
          });
          
          if (!response.ok) throw new Error('Login failed');
          
          const data = await response.json();
          set({ 
            token: data.access_token,
            user: { id: data.user_id, email: data.email },
            loading: false 
          });
          return data;
        } catch (error) {
          set({ error: error.message, loading: false });
          throw error;
        }
      },

      register: async (email, username, password) => {
        set({ loading: true, error: null });
        try {
          const response = await fetch('http://localhost:5000/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, username, password })
          });
          
          if (!response.ok) throw new Error('Registration failed');
          
          const data = await response.json();
          set({ loading: false });
          return data;
        } catch (error) {
          set({ error: error.message, loading: false });
          throw error;
        }
      },

      logout: () => {
        set({ token: null, user: null });
      },

      checkAuth: () => {
        const token = localStorage.getItem('token');
        const user = localStorage.getItem('user');
        if (token && user) {
          set({ token, user: JSON.parse(user) });
        }
      }
    }),
    {
      name: 'auth-store',
      getStorage: () => localStorage
    }
  )
);

export { useAuthStore };
