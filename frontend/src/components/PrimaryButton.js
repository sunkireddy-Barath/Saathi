import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export const PrimaryButton = ({ 
  title, 
  onPress, 
  loading = false, 
  style, 
  textStyle,
  icon: Icon
}) => {
  return (
    <TouchableOpacity 
      onPress={onPress} 
      disabled={loading}
      activeOpacity={0.8}
      style={[styles.container, style]}
    >
      <LinearGradient
        colors={['#4F46E5', '#3B82F6']}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
        style={styles.gradient}
      >
        {loading ? (
          <ActivityIndicator color="#FFFFFF" />
        ) : (
          <>
            {Icon && <Icon color="#FFF" size={20} style={styles.icon} />}
            <Text style={[styles.text, textStyle]}>{title}</Text>
          </>
        )}
      </LinearGradient>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 16,
    overflow: 'hidden',
    shadowColor: '#4F46E5',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 8,
  },
  gradient: {
    height: 56,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 24,
  },
  text: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  icon: {
    marginRight: 8,
  },
});
