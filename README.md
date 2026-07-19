# Saathi 🧵
**An Intelligent Predictive Marketplace and Trust Framework for Handloom Artisans**

Saathi is a production-grade, full-stack platform built to protect traditional handloom artisans from price exploitation and demand uncertainty. 

## Features
- **Fair Price Engine:** Calculates algorithmic minimum price floors using labor, material, and logistics parameters to prevent exploitation.
- **Hybrid Demand Forecasting:** Built-in AI microservice (Scikit-Learn + XGBoost) trained on historical data to predict 30-day demand and recommend inventory actions.
- **Immutable Trust Ledger:** Event-sourced trust scoring that ensures all negotiations, disputes, and reviews permanently influence a user's reputation.
- **Secure Negotiation (Lock & Talk):** WebSockets-based real-time chat room where buyers lock products and negotiate securely, bounded by the Fair Price Floor.
- **Cross-Platform UI:** High-performance React Native (Expo) frontend with a beautiful glassmorphism design, natively supporting iOS, Android, and Web browsers.

## Architecture & Tech Stack
1. **Frontend (`/frontend`):** React Native, Expo, React Navigation, NativeWind/Tailwind, Axios, Gifted Charts.
2. **Backend (`/backend`):** FastAPI, PostgreSQL, SQLAlchemy 2.0 (Async), Alembic, Uvicorn, JWT Auth.
3. **AI Engine (`/ai_engine`):** Python, FastAPI, XGBoost, Pandas, Scikit-learn.

## How to Run Locally

### 1. Start the Backend & AI Engine (Docker)
The backend and AI microservice are fully containerized.
```bash
cd Saathi
docker-compose up --build
```
This command spins up:
- PostgreSQL (Port: `5432`)
- Redis (Port: `6379`)
- FastAPI Backend (Port: `8000`)
- AI Engine API (Port: `8001`)

### 2. Start the Frontend (React Native Expo)
Open a new terminal.
```bash
cd Saathi/frontend
npm install
npx expo start
```
- Press `w` to open the Web App in your browser.
- Or, scan the QR code using the **Expo Go** app on your iPhone or Android device to view the mobile app.

---
*Built with modern layered architecture principles and state-of-the-art UI/UX design.*
