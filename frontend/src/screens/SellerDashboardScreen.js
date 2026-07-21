import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, SafeAreaView, Dimensions, ActivityIndicator } from 'react-native';
import { GlassCard } from '../components/GlassCard';
import { LineChart } from 'react-native-gifted-charts';
import { TrendingUp, Activity, ShieldCheck, Box } from 'lucide-react-native';
import { api } from '../services/api';

const { width } = Dimensions.get('window');

export const SellerDashboardScreen = () => {
  const [trustScore, setTrustScore] = useState(100);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [forecastData, setForecastData] = useState([]);
  const [recommendation, setRecommendation] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const trustResponse = await api.get('/trust/score');
      setTrustScore(trustResponse.data.current_score);

      const statsResponse = await api.get('/seller/dashboard');
      setStats(statsResponse.data);

      const predResponse = await api.post('/forecast/predict', {
        product_id: '1',
        category: 'Silk'
      });
      
      const formattedChartData = predResponse.data.forecast_data.map(item => ({
        value: item.predicted_demand,
        label: `Day ${item.day}`
      }));
      
      setForecastData(formattedChartData);
      setRecommendation({
        title: predResponse.data.best_selling_window,
        desc: predResponse.data.recommendation
      });
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={[styles.container, { justifyContent: 'center', alignItems: 'center' }]}>
        <ActivityIndicator size="large" color="#10B981" />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Hello, Artisan!</Text>
            <Text style={styles.subtitle}>Here is your shop's performance.</Text>
          </View>
          <View style={[styles.trustBadge, trustScore < 50 && { borderColor: '#EF4444', backgroundColor: 'rgba(239, 68, 68, 0.1)' }]}>
            <ShieldCheck color={trustScore >= 50 ? "#10B981" : "#EF4444"} size={20} />
            <Text style={[styles.trustText, trustScore < 50 && { color: '#EF4444' }]}>{trustScore} Trust</Text>
          </View>
        </View>

        {/* Stats Row */}
        <View style={styles.statsRow}>
          <GlassCard style={styles.statCard}>
            <Activity color="#4F46E5" size={24} />
            <Text style={styles.statLabel}>Active Listings</Text>
            <Text style={styles.statValue}>{stats?.active_products || 0}</Text>
          </GlassCard>
          
          <GlassCard style={styles.statCard}>
            <TrendingUp color="#10B981" size={24} />
            <Text style={styles.statLabel}>Revenue (INR)</Text>
            <Text style={styles.statValue}>₹{stats?.total_revenue || 0}</Text>
          </GlassCard>
        </View>

        {/* Demand Forecast Chart */}
        <GlassCard style={styles.chartCard}>
          <Text style={styles.cardTitle}>AI Demand Forecast (Next 7 Days)</Text>
          <Text style={styles.cardSubtitle}>Confidence Score: 85%</Text>
          
          <View style={styles.chartContainer}>
            <LineChart
              data={forecastData}
              color="#4F46E5"
              thickness={3}
              dataPointsColor="#10B981"
              hideRules
              yAxisColor="#334155"
              xAxisColor="#334155"
              yAxisTextStyle={{ color: '#94A3B8' }}
              xAxisLabelTextStyle={{ color: '#94A3B8' }}
              width={width > 600 ? 500 : width - 100}
              height={180}
              isAnimated
              curved
            />
          </View>
        </GlassCard>

        {/* Fair Price Engine Recommendations */}
        <GlassCard style={styles.actionCard}>
          <Text style={styles.cardTitle}>Smart Selling Window</Text>
          <View style={styles.actionRow}>
            <Box color="#F59E0B" size={24} />
            <View style={styles.actionTextContainer}>
              <Text style={styles.actionTextMain}>{recommendation?.title || "Monitoring Market"}</Text>
              <Text style={styles.actionTextSub}>{recommendation?.desc || "Gathering more data for recommendations."}</Text>
            </View>
          </View>
        </GlassCard>

      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
  scrollContent: {
    padding: 24,
    paddingBottom: 40,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 32,
  },
  greeting: {
    fontSize: 28,
    fontWeight: '700',
    color: '#F8FAFC',
  },
  subtitle: {
    fontSize: 16,
    color: '#94A3B8',
    marginTop: 4,
  },
  trustBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(16, 185, 129, 0.3)',
  },
  trustText: {
    color: '#10B981',
    fontWeight: '700',
    marginLeft: 6,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  statCard: {
    flex: 1,
    marginHorizontal: 4,
    padding: 16,
  },
  statLabel: {
    color: '#94A3B8',
    fontSize: 14,
    marginTop: 12,
  },
  statValue: {
    color: '#F8FAFC',
    fontSize: 24,
    fontWeight: '700',
    marginTop: 4,
  },
  chartCard: {
    marginBottom: 24,
  },
  chartContainer: {
    marginTop: 16,
    alignItems: 'center',
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#F8FAFC',
  },
  cardSubtitle: {
    fontSize: 14,
    color: '#10B981',
    marginTop: 4,
  },
  actionCard: {
    backgroundColor: 'rgba(30, 41, 59, 0.8)',
  },
  actionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 16,
  },
  actionTextContainer: {
    marginLeft: 16,
    flex: 1,
  },
  actionTextMain: {
    color: '#F8FAFC',
    fontSize: 16,
    fontWeight: '600',
  },
  actionTextSub: {
    color: '#94A3B8',
    fontSize: 14,
    marginTop: 4,
  },
});
