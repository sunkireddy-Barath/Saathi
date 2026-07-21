import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, SafeAreaView, Dimensions, ActivityIndicator, Alert } from 'react-native';
import { Search } from 'lucide-react-native';
import { CustomInput } from '../components/CustomInput';
import { ProductCard } from '../components/ProductCard';
import { api } from '../services/api';

const { width } = Dimensions.get('window');

export const MarketplaceScreen = ({ navigation }) => {
  const [search, setSearch] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, [search]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const response = await api.get('/marketplace/products', {
        params: { search: search || undefined }
      });
      setProducts(response.data.items || []);
    } catch (error) {
      console.error('Failed to fetch products:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Marketplace</Text>
        <Text style={styles.subtitle}>Discover authentic handlooms.</Text>
      </View>

      <View style={styles.searchContainer}>
        <CustomInput 
          icon={Search}
          placeholder="Search fabrics, artisans, or regions..."
          value={search}
          onChangeText={setSearch}
        />
      </View>

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#4F46E5" />
        </View>
      ) : (
        <FlatList
          data={products}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <ProductCard 
              product={item} 
              onPress={async () => {
                if (item.status === 'locked') {
                  Alert.alert("Already Locked", "Another buyer is currently negotiating for this item.");
                  return;
                }
                try {
                  const response = await api.post('/negotiation/lock', { product_id: item.id });
                  navigation.navigate('Chat', { negotiation: response.data, product: item });
                } catch (error) {
                  Alert.alert("Error", error.response?.data?.detail || "Failed to lock the deal.");
                }
              }}
            />
          )}
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
          ListEmptyComponent={
            <Text style={styles.emptyText}>No products found.</Text>
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
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: '#F8FAFC',
  },
  subtitle: {
    fontSize: 16,
    color: '#94A3B8',
    marginTop: 4,
  },
  searchContainer: {
    paddingHorizontal: 24,
  },
  listContent: {
    padding: 24,
    paddingBottom: 100, // accommodate bottom tab bar
  },
});
