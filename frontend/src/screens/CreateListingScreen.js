import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  SafeAreaView, 
  KeyboardAvoidingView, 
  Platform,
  Alert 
} from 'react-native';
import { PackagePlus, HandCoins, Clock, Truck, PlusSquare } from 'lucide-react-native';
import { GlassCard } from '../components/GlassCard';
import { CustomInput } from '../components/CustomInput';
import { PrimaryButton } from '../components/PrimaryButton';
import { api } from '../services/api';

export const CreateListingScreen = ({ navigation }) => {
  const [loading, setLoading] = useState(false);
  
  // Basic info
  const [name, setName] = useState('');
  const [fabricType, setFabricType] = useState('silk'); // Default to silk
  
  // Cost inputs
  const [materialCost, setMaterialCost] = useState('');
  const [laborHours, setLaborHours] = useState('');
  const [dyeCost, setDyeCost] = useState('');
  const [transportCost, setTransportCost] = useState('');
  const [wastageCost, setWastageCost] = useState('');
  const [profitMargin, setProfitMargin] = useState('');
  const [sellingPrice, setSellingPrice] = useState('');

  // Fixed constant for MVP
  const REGIONAL_WAGE_PER_HOUR = 150; 

  // Calculate live Fair Price
  const mCost = parseFloat(materialCost) || 0;
  const lHours = parseFloat(laborHours) || 0;
  const dCost = parseFloat(dyeCost) || 0;
  const tCost = parseFloat(transportCost) || 0;
  const wCost = parseFloat(wastageCost) || 0;
  const pMargin = parseFloat(profitMargin) || 0;
  
  const laborCost = lHours * REGIONAL_WAGE_PER_HOUR;
  const baseCost = mCost + laborCost + dCost + tCost + wCost;
  const fairPrice = baseCost + pMargin;

  const handleSubmit = async () => {
    if (!name) {
      Alert.alert("Error", "Product name is required.");
      return;
    }
    
    const sPrice = parseFloat(sellingPrice) || 0;
    if (sPrice < fairPrice) {
      Alert.alert("Fair Price Violation", `You cannot list this item below the calculated Fair Price Floor of ₹${fairPrice}. Protect your labor!`);
      return;
    }

    setLoading(true);
    try {
      const payload = {
        name,
        description: "Authentic handloom product.",
        fabric_type: fabricType,
        material_cost: mCost,
        labor_hours: lHours,
        labor_cost: laborCost,
        dye_cost: dCost,
        transport_cost: tCost,
        wastage_cost: wCost,
        profit_margin: pMargin,
        selling_price: sPrice
      };

      await api.post('/marketplace/products', payload);
      Alert.alert("Success", "Product listed successfully!");
      navigation.goBack(); // Go back to dashboard
    } catch (error) {
      console.error(error.response?.data || error);
      Alert.alert("Error", "Failed to create listing.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView contentContainerStyle={styles.scrollContent}>
          <Text style={styles.headerTitle}>New Listing</Text>
          <Text style={styles.headerSubtitle}>Calculate your Fair Price Floor</Text>

          <GlassCard style={styles.card}>
            <CustomInput
              label="Product Name"
              icon={PackagePlus}
              placeholder="e.g. Banarasi Silk Saree"
              value={name}
              onChangeText={setName}
            />
            
            <CustomInput
              label="Fabric Type (e.g., silk, cotton, chanderi)"
              icon={PackagePlus}
              placeholder="silk"
              value={fabricType}
              onChangeText={setFabricType}
              autoCapitalize="none"
            />
          </GlassCard>

          <Text style={styles.sectionTitle}>Cost Breakdown (₹)</Text>
          <GlassCard style={styles.card}>
            <CustomInput
              label="Raw Material Cost"
              icon={HandCoins}
              placeholder="0"
              keyboardType="numeric"
              value={materialCost}
              onChangeText={setMaterialCost}
            />
            <CustomInput
              label="Labor Hours Spent"
              icon={Clock}
              placeholder="0"
              keyboardType="numeric"
              value={laborHours}
              onChangeText={setLaborHours}
            />
            <CustomInput
              label="Dyes & Colors Cost"
              icon={HandCoins}
              placeholder="0"
              keyboardType="numeric"
              value={dyeCost}
              onChangeText={setDyeCost}
            />
            <CustomInput
              label="Transport/Logistics"
              icon={Truck}
              placeholder="0"
              keyboardType="numeric"
              value={transportCost}
              onChangeText={setTransportCost}
            />
            <CustomInput
              label="Estimated Wastage Cost"
              icon={HandCoins}
              placeholder="0"
              keyboardType="numeric"
              value={wastageCost}
              onChangeText={setWastageCost}
            />
            <CustomInput
              label="Desired Profit Margin"
              icon={PlusSquare}
              placeholder="0"
              keyboardType="numeric"
              value={profitMargin}
              onChangeText={setProfitMargin}
            />
          </GlassCard>

          <GlassCard style={styles.summaryCard} intensity={60}>
            <Text style={styles.summaryTitle}>Fair Price Floor</Text>
            <Text style={styles.fairPriceText}>₹{fairPrice.toFixed(2)}</Text>
            <Text style={styles.summarySubtitle}>Base Cost: ₹{baseCost.toFixed(2)} | Labor: ₹{laborCost.toFixed(2)}</Text>
            
            <View style={{ marginTop: 20 }}>
              <CustomInput
                label="Your Listing Price"
                icon={HandCoins}
                placeholder={`Min: ₹${fairPrice}`}
                keyboardType="numeric"
                value={sellingPrice}
                onChangeText={setSellingPrice}
              />
            </View>

            <PrimaryButton 
              title="Publish Listing" 
              onPress={handleSubmit} 
              loading={loading}
            />
          </GlassCard>

        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    padding: 20,
    paddingBottom: 40,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: '800',
    color: '#F8FAFC',
    marginTop: 10,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#94A3B8',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#F8FAFC',
    marginTop: 10,
    marginBottom: 10,
    marginLeft: 4,
  },
  card: {
    marginBottom: 20,
  },
  summaryCard: {
    padding: 24,
    borderColor: '#4F46E5',
    borderWidth: 1,
  },
  summaryTitle: {
    color: '#E2E8F0',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
  },
  fairPriceText: {
    color: '#10B981',
    fontSize: 42,
    fontWeight: '800',
    textAlign: 'center',
    marginVertical: 10,
  },
  summarySubtitle: {
    color: '#94A3B8',
    fontSize: 12,
    textAlign: 'center',
    marginBottom: 10,
  }
});
