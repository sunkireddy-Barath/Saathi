import React, { useState, useEffect, useRef, useContext } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TextInput, 
  TouchableOpacity, 
  FlatList, 
  KeyboardAvoidingView, 
  Platform,
  SafeAreaView,
  Alert
} from 'react-native';
import { Send, ShieldAlert, ArrowLeft } from 'lucide-react-native';
import { AuthContext } from '../context/AuthContext';
import { api } from '../services/api';

export const ChatScreen = ({ route, navigation }) => {
  const { negotiation, product } = route.params;
  const { user, token } = useContext(AuthContext);
  
  const [messages, setMessages] = useState([]);
  const [inputMsg, setInputMsg] = useState('');
  const [offerAmount, setOfferAmount] = useState('');
  const ws = useRef(null);
  const flatListRef = useRef(null);

  useEffect(() => {
    // 1. Fetch chat history
    fetchHistory();

    // 2. Determine WebSocket URL (replace http:// with ws://)
    const baseUrl = api.defaults.baseURL;
    const wsUrl = baseUrl.replace('http://', 'ws://').replace('https://', 'wss://');
    
    // 3. Connect to WebSocket
    ws.current = new WebSocket(`${wsUrl}/ws/chat/${negotiation.id}?token=${token}`);

    ws.current.onopen = () => {
      console.log('Connected to Chat WS');
    };

    ws.current.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data.error) {
          Alert.alert("Error", data.error);
        } else {
          setMessages(prev => [...prev, data]);
        }
      } catch (err) {
        // Handle raw string fallbacks if any
        if (typeof e.data === 'string' && e.data.includes("error")) {
             Alert.alert("System", e.data);
        }
      }
    };

    ws.current.onerror = (e) => {
      console.log('WS Error', e.message);
    };

    return () => {
      if (ws.current) ws.current.close();
    };
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await api.get(`/negotiation/${negotiation.id}`);
      setMessages(response.data.messages || []);
    } catch (error) {
      console.error("Failed to load history", error);
    }
  };

  const sendMessage = () => {
    if (!inputMsg.trim()) return;
    
    const payload = {
      type: 'text',
      content: inputMsg,
    };
    
    ws.current.send(JSON.stringify(payload));
    setInputMsg('');
  };

  const sendOffer = () => {
    const amount = parseFloat(offerAmount);
    if (isNaN(amount) || amount <= 0) return;

    // ALGORITHMIC PROTECTION (Fair Price Floor)
    if (user.role === 'buyer' && amount < negotiation.fair_price_floor) {
      Alert.alert(
        "Offer Rejected", 
        `You cannot offer below the calculated Fair Price Floor of ₹${negotiation.fair_price_floor}. This strictly protects the artisan from exploitation.`
      );
      return;
    }

    const payload = {
      type: 'offer',
      content: `Made an offer of ₹${amount}`,
      offer_amount: amount
    };

    ws.current.send(JSON.stringify(payload));
    setOfferAmount('');
  };

  const renderMessage = ({ item }) => {
    const isMe = item.sender_id === user.id;
    return (
      <View style={[styles.msgContainer, isMe ? styles.myMsg : styles.theirMsg]}>
        {item.type === 'offer' && (
          <ShieldAlert color={isMe ? "#FFF" : "#4F46E5"} size={16} style={{ marginBottom: 4 }} />
        )}
        <Text style={[styles.msgText, isMe ? styles.myText : styles.theirText]}>
          {item.content}
        </Text>
        <Text style={[styles.timeText, isMe ? styles.myTime : styles.theirTime]}>
          {new Date(item.created_at || Date.now()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </Text>
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <ArrowLeft color="#F8FAFC" size={24} />
        </TouchableOpacity>
        <View style={styles.headerText}>
          <Text style={styles.headerTitle}>{product?.name || "Negotiation"}</Text>
          <Text style={styles.headerSubtitle}>
            Floor: ₹{negotiation.fair_price_floor} | Status: {negotiation.status}
          </Text>
        </View>
      </View>

      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={item => item.id || item.created_at}
        renderItem={renderMessage}
        contentContainerStyle={styles.chatList}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
      />

      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'} 
      >
        <View style={styles.inputArea}>
          {/* Offer Bar */}
          <View style={styles.offerRow}>
            <TextInput
              style={styles.offerInput}
              placeholder="₹ Offer Amount"
              placeholderTextColor="#94A3B8"
              keyboardType="numeric"
              value={offerAmount}
              onChangeText={setOfferAmount}
            />
            <TouchableOpacity style={styles.offerBtn} onPress={sendOffer}>
              <Text style={styles.offerBtnText}>Send Offer</Text>
            </TouchableOpacity>
          </View>

          {/* Chat Bar */}
          <View style={styles.chatRow}>
            <TextInput
              style={styles.chatInput}
              placeholder="Type a message..."
              placeholderTextColor="#94A3B8"
              value={inputMsg}
              onChangeText={setInputMsg}
              multiline
            />
            <TouchableOpacity style={styles.sendBtn} onPress={sendMessage}>
              <Send color="#FFF" size={20} />
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0F172A' },
  header: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    padding: 16, 
    borderBottomWidth: 1, 
    borderBottomColor: '#1E293B' 
  },
  backBtn: { marginRight: 16 },
  headerTitle: { color: '#FFF', fontSize: 18, fontWeight: '700' },
  headerSubtitle: { color: '#10B981', fontSize: 12, fontWeight: '600' },
  chatList: { padding: 16, flexGrow: 1, justifyContent: 'flex-end' },
  msgContainer: { 
    maxWidth: '80%', 
    padding: 12, 
    borderRadius: 16, 
    marginBottom: 12 
  },
  myMsg: { 
    alignSelf: 'flex-end', 
    backgroundColor: '#4F46E5', 
    borderBottomRightRadius: 4 
  },
  theirMsg: { 
    alignSelf: 'flex-start', 
    backgroundColor: '#1E293B', 
    borderBottomLeftRadius: 4 
  },
  msgText: { fontSize: 15 },
  myText: { color: '#FFF' },
  theirText: { color: '#E2E8F0' },
  timeText: { fontSize: 10, marginTop: 4, alignSelf: 'flex-end' },
  myTime: { color: 'rgba(255,255,255,0.7)' },
  theirTime: { color: '#94A3B8' },
  inputArea: { 
    padding: 12, 
    backgroundColor: '#1E293B',
    borderTopWidth: 1,
    borderTopColor: '#334155'
  },
  offerRow: { 
    flexDirection: 'row', 
    marginBottom: 12,
    alignItems: 'center'
  },
  offerInput: { 
    flex: 1, 
    backgroundColor: '#0F172A', 
    color: '#FFF', 
    height: 44, 
    borderRadius: 22, 
    paddingHorizontal: 16,
    marginRight: 8,
    borderWidth: 1,
    borderColor: '#4F46E5'
  },
  offerBtn: { 
    backgroundColor: '#10B981', 
    height: 44, 
    paddingHorizontal: 20, 
    borderRadius: 22, 
    justifyContent: 'center' 
  },
  offerBtnText: { color: '#FFF', fontWeight: '700' },
  chatRow: { flexDirection: 'row', alignItems: 'center' },
  chatInput: { 
    flex: 1, 
    backgroundColor: '#0F172A', 
    color: '#FFF', 
    minHeight: 44, 
    maxHeight: 100, 
    borderRadius: 22, 
    paddingHorizontal: 16, 
    paddingTop: 12, 
    paddingBottom: 12,
    marginRight: 8 
  },
  sendBtn: { 
    backgroundColor: '#4F46E5', 
    width: 44, 
    height: 44, 
    borderRadius: 22, 
    justifyContent: 'center', 
    alignItems: 'center' 
  }
});
