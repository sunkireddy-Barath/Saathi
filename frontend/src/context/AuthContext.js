import React, { createContext, useState, useEffect } from 'react';
import { api, setAuthToken } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, retrieve stored token here to auto-login
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      console.log('[AuthContext] Attempting login for:', email);
      const response = await api.post('/auth/login', { email, password });
      const { access_token } = response.data;
      setAuthToken(access_token);
      setToken(access_token);
      
      console.log('[AuthContext] Login token received. Fetching user profile...');
      const userResponse = await api.get('/auth/me');
      console.log('[AuthContext] Authenticated user profile:', userResponse.data);
      setUser(userResponse.data);
      return true;
    } catch (error) {
      console.error('[AuthContext] Login error:', error.response?.data || error.message);
      throw error;
    }
  };

  const signup = async (name, email, password, role) => {
    try {
      console.log('[AuthContext] Posting signup data:', { name, email, role });
      await api.post('/auth/signup', { name, email, password, role });
      console.log('[AuthContext] Signup post successful. Auto-logging in...');
      return await login(email, password);
    } catch (error) {
      console.error('[AuthContext] Signup API error:', error.response?.data || error.message);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setAuthToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, signup, logout, setLoading }}>
      {children}
    </AuthContext.Provider>
  );
};
