import React, { useContext, useState, useEffect } from 'react';
import { View, Text, StyleSheet, SafeAreaView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { AuthContext } from '../context/AuthContext';
import { api } from '../services/api';
import { ShieldCheck, User } from 'lucide-react-native';

export const ProfileScreen = () => {
  const { user, logout } = useContext(AuthContext);
  const [trustScore, setTrustScore] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrustScore();
  }, []);

  const fetchTrustScore = async () => {
    try {
      setLoading(true);
      const response = await api.get('/trust/score');
      setTrustScore(response.data.current_score);
    } catch (error) {
      console.error('Failed to fetch trust score:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Profile</Text>
        <Text style={styles.subtitle}>Manage your account.</Text>
      </View>
      <View style={styles.content}>
        <View style={styles.profileCard}>
          <View style={styles.avatarPlaceholder}>
            <User color="#94A3B8" size={40} />
          </View>
          <Text style={styles.email}>{user?.email || 'user@example.com'}</Text>
          <Text style={styles.role}>{user?.role?.toUpperCase() || 'USER'}</Text>
          
          {loading ? (
            <ActivityIndicator style={{ marginTop: 16 }} color="#4F46E5" />
          ) : (
            trustScore !== null && (
              <View style={[styles.trustBadge, trustScore < 50 && { borderColor: '#EF4444', backgroundColor: 'rgba(239, 68, 68, 0.1)' }]}>
                <ShieldCheck color={trustScore >= 50 ? "#10B981" : "#EF4444"} size={20} />
                <Text style={[styles.trustText, trustScore < 50 && { color: '#EF4444' }]}>{trustScore} Trust Score</Text>
              </View>
            )
          )}
        </View>

        <TouchableOpacity style={styles.button} onPress={logout}>
          <Text style={styles.buttonText}>Logout</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { padding: 24 },
  title: { fontSize: 32, fontWeight: '800', color: '#F8FAFC' },
  subtitle: { fontSize: 16, color: '#94A3B8', marginTop: 4 },
  content: { padding: 24 },
  profileCard: { backgroundColor: '#1E293B', padding: 24, borderRadius: 16, alignItems: 'center', marginBottom: 24 },
  avatarPlaceholder: { width: 80, height: 80, borderRadius: 40, backgroundColor: '#334155', justifyContent: 'center', alignItems: 'center', marginBottom: 16 },
  email: { fontSize: 20, fontWeight: '700', color: '#F8FAFC' },
  role: { fontSize: 14, color: '#94A3B8', marginTop: 4, letterSpacing: 1 },
  trustBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: 'rgba(16, 185, 129, 0.1)', paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20, borderWidth: 1, borderColor: 'rgba(16, 185, 129, 0.3)', marginTop: 16 },
  trustText: { color: '#10B981', fontWeight: '700', marginLeft: 8 },
  button: { backgroundColor: '#EF4444', padding: 16, borderRadius: 12, alignItems: 'center' },
  buttonText: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
});
