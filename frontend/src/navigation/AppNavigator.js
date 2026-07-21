import React, { useContext } from 'react';
import { NavigationContainer, DarkTheme } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, ShoppingBag, LayoutDashboard, User, PlusSquare } from 'lucide-react-native';

import { AuthContext } from '../context/AuthContext';
import { LoginScreen } from '../screens/LoginScreen';
import { SignupScreen } from '../screens/SignupScreen';
import { MarketplaceScreen } from '../screens/MarketplaceScreen';
import { SellerDashboardScreen } from '../screens/SellerDashboardScreen';
import { CreateListingScreen } from '../screens/CreateListingScreen';
import { ChatScreen } from '../screens/ChatScreen';
import { AdminDashboardScreen } from '../screens/AdminDashboardScreen';
import { OrdersScreen } from '../screens/OrdersScreen';
import { InventoryScreen } from '../screens/InventoryScreen';
import { ProfileScreen } from '../screens/ProfileScreen';
import { ShieldAlert } from 'lucide-react-native';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();
const AuthStack = createNativeStackNavigator();

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

const AdminTabs = () => (
  <Tab.Navigator
    screenOptions={{
      headerShown: false,
      tabBarStyle: { backgroundColor: '#1E293B', borderTopWidth: 0, height: 60, paddingBottom: 8 },
      tabBarActiveTintColor: '#EF4444', // Red for admin
      tabBarInactiveTintColor: '#64748B',
    }}
  >
    <Tab.Screen 
      name="Moderation" 
      component={AdminDashboardScreen} 
      options={{ tabBarIcon: ({ color, size }) => <ShieldAlert color={color} size={size} /> }}
    />
  </Tab.Navigator>
);

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
      component={OrdersScreen} 
      options={{ tabBarIcon: ({ color, size }) => <ShoppingBag color={color} size={size} /> }}
    />
    <Tab.Screen 
      name="Profile" 
      component={ProfileScreen} 
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
      name="New Listing" 
      component={CreateListingScreen} 
      options={{ tabBarIcon: ({ color, size }) => <PlusSquare color={color} size={size} /> }}
    />
    <Tab.Screen 
      name="Inventory" 
      component={InventoryScreen} 
      options={{ tabBarIcon: ({ color, size }) => <ShoppingBag color={color} size={size} /> }}
    />
    <Tab.Screen 
      name="Profile" 
      component={ProfileScreen} 
      options={{ tabBarIcon: ({ color, size }) => <User color={color} size={size} /> }}
    />
  </Tab.Navigator>
);

const AuthNavigator = () => (
  <AuthStack.Navigator screenOptions={{ headerShown: false }}>
    <AuthStack.Screen name="Login" component={LoginScreen} />
    <AuthStack.Screen name="Signup" component={SignupScreen} />
  </AuthStack.Navigator>
);

export const AppNavigator = () => {
  const { user } = useContext(AuthContext);

  return (
    <NavigationContainer theme={customDarkTheme}>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {user ? (
          <Stack.Group>
            {user.role === 'admin' ? (
              <Stack.Screen name="AdminRoot" component={AdminTabs} />
            ) : user.role === 'seller' ? (
              <Stack.Screen name="SellerRoot" component={SellerTabs} />
            ) : (
              <Stack.Screen name="BuyerRoot" component={BuyerTabs} />
            )}
            <Stack.Screen name="Chat" component={ChatScreen} />
          </Stack.Group>
        ) : (
          <Stack.Screen name="AuthRoot" component={AuthNavigator} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};
