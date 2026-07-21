import React, { useContext } from 'react';
import { View, TouchableOpacity, Text, useWindowDimensions } from 'react-native';
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

const Sidebar = ({ state, descriptors, navigation, activeColor }) => {
  return (
    <View style={{
      position: 'absolute',
      left: 0,
      top: 0,
      bottom: 0,
      width: 250,
      backgroundColor: '#1E293B',
      borderRightWidth: 1,
      borderColor: '#334155',
      paddingTop: 40,
    }}>
      {state.routes.map((route, index) => {
        const { options } = descriptors[route.key];
        const label = options.tabBarLabel !== undefined
            ? options.tabBarLabel
            : options.title !== undefined
            ? options.title
            : route.name;
        const isFocused = state.index === index;

        const onPress = () => {
          const event = navigation.emit({
            type: 'tabPress',
            target: route.key,
            canPreventDefault: true,
          });
          if (!isFocused && !event.defaultPrevented) {
            navigation.navigate(route.name);
          }
        };

        const color = isFocused ? activeColor : '#64748B';

        return (
          <TouchableOpacity
            key={index}
            accessibilityRole="button"
            accessibilityState={isFocused ? { selected: true } : {}}
            onPress={onPress}
            style={{
              flexDirection: 'row',
              alignItems: 'center',
              paddingHorizontal: 20,
              paddingVertical: 15,
              backgroundColor: isFocused ? 'rgba(255,255,255,0.05)' : 'transparent',
              borderLeftWidth: 3,
              borderLeftColor: isFocused ? activeColor : 'transparent',
            }}
          >
            {options.tabBarIcon && options.tabBarIcon({ focused: isFocused, color, size: 24 })}
            <Text style={{ color, marginLeft: 15, fontSize: 16, fontWeight: isFocused ? '600' : '400' }}>
              {label}
            </Text>
          </TouchableOpacity>
        );
      })}
    </View>
  );
};

const getResponsiveTabOptions = (width, activeColor) => {
  const isLargeScreen = width >= 768;
  return {
    headerShown: false,
    sceneStyle: isLargeScreen ? { marginLeft: 250 } : undefined,
    tabBarStyle: isLargeScreen ? { display: 'none' } : { 
      backgroundColor: '#1E293B', 
      borderTopWidth: 0, 
      minHeight: 60, 
      paddingTop: 8 
    },
    tabBarActiveTintColor: activeColor,
    tabBarInactiveTintColor: '#64748B',
  };
};

const AdminTabs = () => {
  const { width } = useWindowDimensions();
  const isLargeScreen = width >= 768;
  return (
    <Tab.Navigator
      tabBar={isLargeScreen ? (props) => <Sidebar {...props} activeColor="#EF4444" /> : undefined}
      screenOptions={getResponsiveTabOptions(width, '#EF4444')}
    >
      <Tab.Screen 
        name="Moderation" 
        component={AdminDashboardScreen} 
        options={{ tabBarIcon: ({ color, size }) => <ShieldAlert color={color} size={size} /> }}
      />
    </Tab.Navigator>
  );
};

const BuyerTabs = () => {
  const { width } = useWindowDimensions();
  const isLargeScreen = width >= 768;
  return (
    <Tab.Navigator
      tabBar={isLargeScreen ? (props) => <Sidebar {...props} activeColor="#4F46E5" /> : undefined}
      screenOptions={getResponsiveTabOptions(width, '#4F46E5')}
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
};

const SellerTabs = () => {
  const { width } = useWindowDimensions();
  const isLargeScreen = width >= 768;
  return (
    <Tab.Navigator
      tabBar={isLargeScreen ? (props) => <Sidebar {...props} activeColor="#10B981" /> : undefined}
      screenOptions={getResponsiveTabOptions(width, '#10B981')}
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
};

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
