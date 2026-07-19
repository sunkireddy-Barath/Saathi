import React, { createContext, useState, useEffect } from 'react';
import { api, setAuthToken } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // In a real app, use SecureStore (expo-secure-store) or AsyncStorage here
  
  const login = async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      const { access_token } = response.data;
      setAuthToken(access_token);
      
      // Fetch user profile
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data);
      return true;
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setAuthToken(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, setLoading }}>
      {children}
    </AuthContext.Provider>
  );
};
