import React from 'react';
import { TextInput, View, Text, StyleSheet } from 'react-native';

export const CustomInput = ({ 
  label, 
  icon: Icon, 
  error, 
  ...props 
}) => {
  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}
      <View style={[styles.inputContainer, error && styles.inputError]}>
        {Icon && <Icon size={20} color="#94A3B8" style={styles.icon} />}
        <TextInput
          style={styles.input}
          placeholderTextColor="#64748B"
          {...props}
        />
      </View>
      {error && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: 20,
  },
  label: {
    color: '#E2E8F0',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
    marginLeft: 4,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(30, 41, 59, 0.7)',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.1)',
    height: 56,
    paddingHorizontal: 16,
  },
  inputError: {
    borderColor: '#EF4444',
  },
  icon: {
    marginRight: 12,
  },
  input: {
    flex: 1,
    color: '#F8FAFC',
    fontSize: 16,
    height: '100%',
  },
  errorText: {
    color: '#EF4444',
    fontSize: 12,
    marginTop: 6,
    marginLeft: 4,
  },
});
