import React, { useState, useContext } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  KeyboardAvoidingView, 
  Platform,
  SafeAreaView,
  Dimensions,
  TouchableOpacity,
  ScrollView
} from 'react-native';
import { Mail, Lock, User, Palette, Briefcase, ArrowRight } from 'lucide-react-native';
import { GlassCard } from '../components/GlassCard';
import { CustomInput } from '../components/CustomInput';
import { PrimaryButton } from '../components/PrimaryButton';
import { AuthContext } from '../context/AuthContext';

const { width } = Dimensions.get('window');

export const SignupScreen = ({ navigation }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('buyer'); // 'buyer' or 'seller'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { signup } = useContext(AuthContext);

  const validatePassword = (pwd) => {
    if (pwd.length < 8) return 'Password must be at least 8 characters long.';
    if (!/[A-Z]/.test(pwd)) return 'Password must contain at least one uppercase letter.';
    if (!/[a-z]/.test(pwd)) return 'Password must contain at least one lowercase letter.';
    if (!/\d/.test(pwd)) return 'Password must contain at least one digit.';
    if (!/[!@#$%^&*(),.?":{}|<>_\-]/.test(pwd)) return 'Password must contain at least one special character.';
    return '';
  };

  const handleSignup = async () => {
    console.log('[SignupScreen] Create Account button clicked with:', { name, email, role });

    if (!name || !email || !password) {
      console.warn('[SignupScreen] Validation error: Missing required fields');
      setError('Please fill in all fields');
      return;
    }

    if (name.length < 2) {
      console.warn('[SignupScreen] Validation error: Name too short');
      setError('Name must be at least 2 characters long.');
      return;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      console.warn('[SignupScreen] Validation error: Invalid email format');
      setError('Please enter a valid email address.');
      return;
    }

    const pwdError = validatePassword(password);
    if (pwdError) {
      console.warn('[SignupScreen] Validation error:', pwdError);
      setError(pwdError);
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      console.log('[SignupScreen] Dispatching signup request...');
      await signup(name, email, password, role);
      console.log('[SignupScreen] Signup completed successfully!');
    } catch (err) {
      const msg = err.response?.data?.detail || 'Registration failed. Check network or email.';
      console.error('[SignupScreen] Signup error:', err.response?.data || err.message);
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      {/* Background blobs for premium styling */}
      <View style={styles.bgBlob1} />
      <View style={styles.bgBlob2} />

      <SafeAreaView style={styles.safeArea}>
        <KeyboardAvoidingView 
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardView}
        >
          <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
            <View style={styles.header}>
              <Text style={styles.logoText}>Saathi</Text>
              <Text style={styles.subtitle}>Join our ethical handloom community</Text>
            </View>

            <GlassCard style={styles.card}>
              <Text style={styles.cardTitle}>Create Account</Text>
              
              <CustomInput
                label="Full Name"
                icon={User}
                placeholder="Enter your name"
                value={name}
                onChangeText={setName}
                autoCapitalize="words"
              />

              <CustomInput
                label="Email Address"
                icon={Mail}
                placeholder="Enter your email"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
              />
              
              <CustomInput
                label="Password"
                icon={Lock}
                placeholder="Choose a strong password"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
              />

              {/* Role Segmented Selector */}
              <Text style={styles.roleLabel}>Choose your account type</Text>
              <View style={styles.roleContainer}>
                {/* Seller Option */}
                <TouchableOpacity 
                  style={[
                    styles.roleCard, 
                    role === 'seller' && styles.roleCardActiveSeller
                  ]} 
                  onPress={() => setRole('seller')}
                  activeOpacity={0.9}
                >
                  <Palette color={role === 'seller' ? '#10B981' : '#64748B'} size={24} />
                  <Text style={[styles.roleCardTitle, role === 'seller' && styles.roleTextActiveSeller]}>
                    Artisan / Weaver
                  </Text>
                  <Text style={styles.roleCardDesc}>I list and sell my authentic textiles.</Text>
                </TouchableOpacity>

                {/* Buyer Option */}
                <TouchableOpacity 
                  style={[
                    styles.roleCard, 
                    role === 'buyer' && styles.roleCardActiveBuyer
                  ]} 
                  onPress={() => setRole('buyer')}
                  activeOpacity={0.9}
                >
                  <Briefcase color={role === 'buyer' ? '#4F46E5' : '#64748B'} size={24} />
                  <Text style={[styles.roleCardTitle, role === 'buyer' && styles.roleTextActiveBuyer]}>
                    Bulk Buyer
                  </Text>
                  <Text style={styles.roleCardDesc}>I procure direct or negotiate orders.</Text>
                </TouchableOpacity>
              </View>

              {error ? <Text style={styles.errorText}>{error}</Text> : null}

              <PrimaryButton
                title="Create Account"
                onPress={handleSignup}
                loading={loading}
                icon={ArrowRight}
                style={{ marginTop: 8 }}
              />
              
              <View style={styles.footer}>
                <Text style={styles.footerText}>Already have an account? </Text>
                <TouchableOpacity onPress={() => navigation.navigate('Login')}>
                  <Text style={styles.footerLink}>Sign in</Text>
                </TouchableOpacity>
              </View>
            </GlassCard>
          </ScrollView>
        </KeyboardAvoidingView>
      </SafeAreaView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
  bgBlob1: {
    position: 'absolute',
    top: -100,
    right: -100,
    width: 300,
    height: 300,
    borderRadius: 150,
    backgroundColor: 'rgba(79, 70, 229, 0.15)',
    transform: [{ scale: 1.5 }],
  },
  bgBlob2: {
    position: 'absolute',
    bottom: -100,
    left: -100,
    width: 300,
    height: 300,
    borderRadius: 150,
    backgroundColor: 'rgba(16, 185, 129, 0.15)',
    transform: [{ scale: 1.5 }],
  },
  safeArea: {
    flex: 1,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    padding: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
    marginTop: 20,
  },
  logoText: {
    fontSize: 42,
    fontWeight: '800',
    color: '#F8FAFC',
    letterSpacing: -1,
  },
  subtitle: {
    fontSize: 16,
    color: '#94A3B8',
    marginTop: 8,
    textAlign: 'center',
  },
  card: {
    width: '100%',
    maxWidth: 400,
    alignSelf: 'center',
    paddingBottom: 24,
  },
  cardTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: '#F8FAFC',
    marginBottom: 24,
  },
  roleLabel: {
    color: '#E2E8F0',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
    marginLeft: 4,
  },
  roleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
    marginBottom: 24,
  },
  roleCard: {
    flex: 1,
    backgroundColor: 'rgba(30, 41, 59, 0.6)',
    borderRadius: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.05)',
    padding: 14,
    alignItems: 'flex-start',
  },
  roleCardActiveSeller: {
    borderColor: '#10B981',
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
  },
  roleCardActiveBuyer: {
    borderColor: '#4F46E5',
    backgroundColor: 'rgba(79, 70, 229, 0.1)',
  },
  roleCardTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: '#94A3B8',
    marginTop: 8,
    marginBottom: 4,
  },
  roleTextActiveSeller: {
    color: '#10B981',
  },
  roleTextActiveBuyer: {
    color: '#6366F1',
  },
  roleCardDesc: {
    fontSize: 11,
    color: '#64748B',
    lineHeight: 14,
  },
  errorText: {
    color: '#EF4444',
    textAlign: 'center',
    marginBottom: 16,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 24,
  },
  footerText: {
    color: '#94A3B8',
  },
  footerLink: {
    color: '#4F46E5',
    fontWeight: '600',
  },
});
