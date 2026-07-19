# Saathi 🧵
**An Intelligent Predictive Marketplace and Trust Framework for Handloom Artisans**

Saathi is a production-grade, full-stack platform built to protect traditional handloom artisans from price exploitation and demand uncertainty. 

## 🏗 System Architecture

The application is built using a modern, decoupled microservices architecture designed for extreme scalability and mobile/web cross-compatibility.

```mermaid
graph TD
    %% Frontend Clients
    subgraph Clients["Frontend Clients"]
        MobileApp["📱 React Native (iOS/Android)"]
        WebApp["💻 React Native (Web)"]
    end

    %% Backend Services
    subgraph Backend["Core Services (Docker)"]
        API["⚡ FastAPI Main Backend (Port 8000)"]
        AIEngine["🧠 AI Demand Engine (Port 8001)"]
        Redis["🗄️ Redis (WebSockets/Cache)"]
    end

    %% Databases
    subgraph Database["External Storage"]
        Supabase[(🐘 Supabase PostgreSQL)]
    end

    %% Connections
    MobileApp -- "REST API / WebSockets" --> API
    WebApp -- "REST API / WebSockets" --> API
    
    API -- "Fetch Predictions (HTTP)" --> AIEngine
    API -- "Async DB Operations" --> Supabase
    API -- "Pub/Sub" --> Redis
    
    AIEngine -- "Train/Read Data" --> Supabase
```

## ✨ Key Features
1. **Fair Price Engine:** Calculates algorithmic minimum price floors using labor, material, and logistics parameters to prevent exploitation.
2. **Hybrid Demand Forecasting:** Built-in AI microservice (Scikit-Learn + XGBoost) trained on historical data to predict 30-day demand and recommend inventory actions.
3. **Immutable Trust Ledger:** Event-sourced trust scoring that ensures all negotiations, disputes, and reviews permanently influence a user's reputation.
4. **Secure Negotiation (Lock & Talk):** WebSockets-based real-time chat room where buyers lock products and negotiate securely, bounded by the Fair Price Floor.
5. **Cross-Platform UI:** High-performance React Native (Expo) frontend with a beautiful glassmorphism design, natively supporting iOS, Android, and Web browsers with completely **dynamic** data (zero mocks).
6. **Supabase Integration:** Fully configured to leverage Supabase as the primary, cloud-hosted PostgreSQL database for real-time capabilities and robust scaling.

---

## 🛠 Technology Stack
- **Frontend (`/frontend`):** React Native, Expo, React Navigation, NativeWind/Tailwind, Axios, Gifted Charts.
- **Backend (`/backend`):** FastAPI, PostgreSQL (via Supabase), SQLAlchemy 2.0 (Async), Alembic, Uvicorn, JWT Auth.
- **AI Engine (`/ai_engine`):** Python, FastAPI, XGBoost, Pandas, Scikit-learn.

---

## 🚀 How to Run Locally

### 1. Database Setup (Supabase)
Saathi uses **Supabase** for its PostgreSQL database.
1. Go to [Supabase](https://supabase.com/) and create a new project.
2. Get your Database Connection String (URI).
3. In `c:\Saathi\backend`, copy `.env.example` to `.env` and paste your Supabase Transaction connection string:
   ```ini
   # Use the Transaction pooler connection string from Supabase
   DATABASE_URL="postgresql+asyncpg://postgres:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
   SYNC_DATABASE_URL="postgresql+psycopg2://postgres:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
   ```

### 2. Start the Backend & AI Engine (Docker)
Ensure Docker is running, then execute:
```bash
cd Saathi
docker-compose up --build
```
This spins up the FastAPI Backend (Port `8000`), the AI Engine API (Port `8001`), and local Redis for WebSocket state management. Note: The local Postgres container in docker-compose has been bypassed to allow direct connection to your Supabase cloud DB.

### 3. Start the Frontend (React Native Expo)
Open a new terminal.
```bash
cd Saathi/frontend
npm install
npx expo start
```
- Press `w` to open the Web App in your browser.
- Or, scan the QR code using the **Expo Go** app on your iPhone or Android device to view the mobile app dynamically fetching real data!
