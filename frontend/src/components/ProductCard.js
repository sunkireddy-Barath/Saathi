import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { GlassCard } from './GlassCard';
import { ShieldCheck, Tag } from 'lucide-react-native';

export const ProductCard = ({ product, onPress }) => {
  return (
    <TouchableOpacity activeOpacity={0.9} onPress={onPress} style={styles.container}>
      <GlassCard style={styles.card} intensity={30}>
        {/* Placeholder Image using UI Faces or Unsplash for beautiful UI */}
        <Image 
          source={{ uri: product.image_url || 'https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=800&q=80' }} 
          style={styles.image}
        />
        
        <View style={styles.content}>
          <View style={styles.titleRow}>
            <Text style={styles.title} numberOfLines={1}>{product.name}</Text>
            <View style={styles.priceContainer}>
              <Text style={styles.price}>₹{product.price}</Text>
            </View>
          </View>

          <Text style={styles.fabricType}>{product.fabric_type}</Text>

          <View style={styles.footer}>
            <View style={styles.artisanContainer}>
              <Text style={styles.artisanName}>{product.artisan_name}</Text>
              {product.trusted && <ShieldCheck color="#10B981" size={16} style={{ marginLeft: 4 }} />}
            </View>
            
            {product.is_locked ? (
              <View style={[styles.badge, styles.lockedBadge]}>
                <Text style={styles.badgeTextLocked}>Locked</Text>
              </View>
            ) : (
              <View style={[styles.badge, styles.availableBadge]}>
                <Text style={styles.badgeTextAvailable}>Negotiate</Text>
              </View>
            )}
          </View>
        </View>
      </GlassCard>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 24,
    width: '100%',
  },
  card: {
    padding: 0, // override default padding for image
  },
  image: {
    width: '100%',
    height: 200,
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
  },
  content: {
    padding: 20,
  },
  titleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  title: {
    flex: 1,
    fontSize: 20,
    fontWeight: '700',
    color: '#F8FAFC',
    marginRight: 16,
  },
  priceContainer: {
    backgroundColor: 'rgba(79, 70, 229, 0.2)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: 'rgba(79, 70, 229, 0.4)',
  },
  price: {
    color: '#818CF8',
    fontWeight: '800',
    fontSize: 16,
  },
  fabricType: {
    color: '#94A3B8',
    fontSize: 14,
    marginTop: 4,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 20,
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.05)',
  },
  artisanContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  artisanName: {
    color: '#CBD5E1',
    fontWeight: '500',
  },
  badge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    borderWidth: 1,
  },
  availableBadge: {
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    borderColor: 'rgba(16, 185, 129, 0.3)',
  },
  badgeTextAvailable: {
    color: '#10B981',
    fontWeight: '600',
    fontSize: 12,
  },
  lockedBadge: {
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
    borderColor: 'rgba(245, 158, 11, 0.3)',
  },
  badgeTextLocked: {
    color: '#F59E0B',
    fontWeight: '600',
    fontSize: 12,
  },
});
