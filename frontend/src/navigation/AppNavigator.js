import React, { useContext } from 'react';
import { NavigationContainer, DarkTheme } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, ShoppingBag, LayoutDashboard, User } from 'lucide-react-native';

import { AuthContext } from '../context/AuthContext';
import { LoginScreen } from '../screens/LoginScreen';
import { MarketplaceScreen } from '../screens/MarketplaceScreen';
import { SellerDashboardScreen } from '../screens/SellerDashboardScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

const customDarkTheme = {
  ...DarkTheme,
  colors: {
    ...DarkTheme.colors,
    background: '#0F172A',
    card: '#1E293B',
    text: '#F8FAFC',
    border: '#334155',
    primary: '#4F46E5',
  },
};

const BuyerTabs = () => (
  <Tab.Navigator
    screenOptions={{
      headerShown: false,
      tabBarStyle: { backgroundColor: '#1E293B', borderTopWidth: 0, height: 60, paddingBottom: 8 },
      tabBarActiveTintColor: '#4F46E5',
      tabBarInactiveTintColor: '#64748B',
    }}
  >
    <Tab.Screen 
      name="Marketplace" 
      component={MarketplaceScreen} 
      options={{ tabBarIcon: ({ color, size }) => <Home color={color} size={size} /> }}
    />
    <Tab.Screen 
      name="Orders" 
      component={MarketplaceScreen} // Placeholder
      options={{ tabBarIcon: ({ color, size }) => <ShoppingBag color={color} size={size} /> }}
    />
    <Tab.Screen 
      name="Profile" 
      component={MarketplaceScreen} // Placeholder
      options={{ tabBarIcon: ({ color, size }) => <User color={color} size={size} /> }}
    />
  </Tab.Navigator>
);

const SellerTabs = () => (
  <Tab.Navigator
    screenOptions={{
      headerShown: false,
      tabBarStyle: { backgroundColor: '#1E293B', borderTopWidth: 0, height: 60, paddingBottom: 8 },
      tabBarActiveTintColor: '#10B981', // Green for sellers
      tabBarInactiveTintColor: '#64748B',
    }}
  >
    <Tab.Screen 
      name="Dashboard" 
      component={SellerDashboardScreen} 
      options={{ tabBarIcon: ({ color, size }) => <LayoutDashboard color={color} size={size} /> }}
    />
    <Tab.Screen 
      name="Inventory" 
      component={SellerDashboardScreen} // Placeholder
      options={{ tabBarIcon: ({ color, size }) => <ShoppingBag color={color} size={size} /> }}
    />
    <Tab.Screen 
      name="Profile" 
      component={SellerDashboardScreen} // Placeholder
      options={{ tabBarIcon: ({ color, size }) => <User color={color} size={size} /> }}
    />
  </Tab.Navigator>
);

export const AppNavigator = () => {
  const { user } = useContext(AuthContext);

  return (
    <NavigationContainer theme={customDarkTheme}>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {user ? (
          user.role === 'seller' ? (
            <Stack.Screen name="SellerRoot" component={SellerTabs} />
          ) : (
            <Stack.Screen name="BuyerRoot" component={BuyerTabs} />
          )
        ) : (
          <Stack.Screen name="AuthRoot" component={LoginScreen} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};
