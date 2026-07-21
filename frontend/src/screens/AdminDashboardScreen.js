import React, { useState, useEffect } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  FlatList, 
  SafeAreaView, 
  ActivityIndicator,
  TouchableOpacity,
  Alert
} from 'react-native';
import { ShieldAlert, CheckCircle, XCircle, AlertTriangle } from 'lucide-react-native';
import { GlassCard } from '../components/GlassCard';
import { PrimaryButton } from '../components/PrimaryButton';
import { api } from '../services/api';

export const AdminDashboardScreen = () => {
  const [disputes, setDisputes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDisputes();
  }, []);

  const fetchDisputes = async () => {
    try {
      setLoading(true);
      const response = await api.get('/disputes/all');
      setDisputes(response.data.items || []);
    } catch (error) {
      console.error('Failed to fetch disputes:', error);
    } finally {
      setLoading(false);
    }
  };

  const resolveDispute = async (disputeId, winner) => {
    try {
      await api.put(`/disputes/${disputeId}/resolve`, {
        winner,
        resolution_notes: `Admin resolved in favor of ${winner}. Auto-trust deducted.`
      });
      Alert.alert("Success", `Dispute resolved in favor of ${winner}. Trust scores updated!`);
      fetchDisputes();
    } catch (error) {
      Alert.alert("Error", error.response?.data?.detail || "Failed to resolve dispute.");
    }
  };

  const renderDispute = ({ item }) => {
    return (
      <GlassCard style={styles.card} intensity={40}>
        <View style={styles.cardHeader}>
          <ShieldAlert color="#EF4444" size={24} />
          <Text style={styles.disputeTitle}>Dispute #{item.id.slice(0,8)}</Text>
        </View>
        
        <View style={styles.detailsRow}>
          <Text style={styles.label}>Status:</Text>
          <Text style={styles.value}>{item.status.toUpperCase()}</Text>
        </View>
        <View style={styles.detailsRow}>
          <Text style={styles.label}>Reason:</Text>
          <Text style={styles.value}>{item.reason_category}</Text>
        </View>
        
        <Text style={styles.descText}>{item.description}</Text>

        {item.status !== 'resolved' && item.status !== 'closed' && (
          <View style={styles.actionRow}>
            <TouchableOpacity 
              style={[styles.actionBtn, { backgroundColor: 'rgba(16, 185, 129, 0.2)', borderColor: '#10B981' }]}
              onPress={() => resolveDispute(item.id, 'seller')}
            >
              <CheckCircle color="#10B981" size={18} style={{marginRight: 6}} />
              <Text style={{color: '#10B981', fontWeight: 'bold'}}>Favor Seller</Text>
            </TouchableOpacity>

            <TouchableOpacity 
              style={[styles.actionBtn, { backgroundColor: 'rgba(59, 130, 246, 0.2)', borderColor: '#3B82F6' }]}
              onPress={() => resolveDispute(item.id, 'buyer')}
            >
              <CheckCircle color="#3B82F6" size={18} style={{marginRight: 6}} />
              <Text style={{color: '#3B82F6', fontWeight: 'bold'}}>Favor Buyer</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={[styles.actionBtn, { backgroundColor: 'rgba(245, 158, 11, 0.2)', borderColor: '#F59E0B' }]}
              onPress={() => resolveDispute(item.id, 'split')}
            >
              <AlertTriangle color="#F59E0B" size={18} style={{marginRight: 6}} />
              <Text style={{color: '#F59E0B', fontWeight: 'bold'}}>Split Blame</Text>
            </TouchableOpacity>
          </View>
        )}
      </GlassCard>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Moderator Terminal</Text>
        <Text style={styles.subtitle}>Enforce the Trust Framework</Text>
      </View>

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#EF4444" />
        </View>
      ) : (
        <FlatList
          data={disputes}
          keyExtractor={(item) => item.id}
          renderItem={renderDispute}
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <CheckCircle color="#10B981" size={48} />
              <Text style={styles.emptyText}>Zero active disputes!</Text>
              <Text style={styles.emptySub}>The marketplace is safe.</Text>
            </View>
          }
        />
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
  header: {
    paddingHorizontal: 24,
    paddingTop: 24,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#1E293B',
  },
  title: {
    fontSize: 28,
    fontWeight: '800',
    color: '#EF4444', // Red for admin
  },
  subtitle: {
    fontSize: 14,
    color: '#94A3B8',
    marginTop: 4,
  },
  listContent: {
    padding: 24,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    marginBottom: 16,
    padding: 20,
    borderColor: '#334155',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  disputeTitle: {
    color: '#F8FAFC',
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 12,
  },
  detailsRow: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  label: {
    color: '#94A3B8',
    width: 70,
    fontWeight: '600',
  },
  value: {
    color: '#F8FAFC',
    flex: 1,
  },
  descText: {
    color: '#CBD5E1',
    fontStyle: 'italic',
    marginTop: 8,
    marginBottom: 20,
    backgroundColor: 'rgba(0,0,0,0.2)',
    padding: 12,
    borderRadius: 8,
  },
  actionRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionBtn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderRadius: 8,
    paddingVertical: 10,
    marginHorizontal: 4,
  },
  emptyContainer: {
    alignItems: 'center',
    marginTop: 60,
  },
  emptyText: {
    color: '#F8FAFC',
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 16,
  },
  emptySub: {
    color: '#94A3B8',
    marginTop: 8,
  }
});
