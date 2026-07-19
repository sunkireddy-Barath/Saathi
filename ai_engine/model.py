import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

class HybridDemandForecaster:
    def __init__(self):
        self.model = xgb.XGBRegressor(
            objective='reg:squarederror', 
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=5
        )
        self.is_trained = False
        
    def train(self, data_path='data/historical_sales.csv'):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file {data_path} not found. Run generate_data.py first.")
            
        print("Loading training data...")
        df = pd.read_csv(data_path)
        
        # Feature Engineering (One-Hot Encoding for category)
        df = pd.get_dummies(df, columns=['category'], drop_first=True)
        
        # Features and Target
        features = [col for col in df.columns if col not in ['date', 'demand', 'price_inr']]
        X = df[features]
        y = df['demand']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Training XGBoost Demand Forecaster...")
        self.model.fit(X_train, y_train)
        
        preds = self.model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        print(f"Model trained successfully. Test RMSE: {rmse:.2f}")
        
        # Save model and feature columns
        os.makedirs('models', exist_ok=True)
        joblib.dump({'model': self.model, 'features': features}, 'models/xgboost_forecaster.pkl')
        self.is_trained = True
        
    def load_model(self):
        if os.path.exists('models/xgboost_forecaster.pkl'):
            artifact = joblib.load('models/xgboost_forecaster.pkl')
            self.model = artifact['model']
            self.features = artifact['features']
            self.is_trained = True
        else:
            raise FileNotFoundError("Model file not found. Train the model first.")

    def predict_next_n_days(self, category: str, n_days: int = 30):
        if not self.is_trained:
            self.load_model()
            
        # Generate future dates
        from datetime import datetime, timedelta
        base_date = datetime.today()
        
        future_data = []
        for i in range(1, n_days + 1):
            target_date = base_date + timedelta(days=i)
            row = {
                'month': target_date.month,
                'day_of_week': target_date.weekday(),
                'is_weekend': 1 if target_date.weekday() >= 5 else 0,
            }
            # Add one-hot encoded categories
            for feat in self.features:
                if feat.startswith('category_'):
                    row[feat] = 1 if feat == f'category_{category}' else 0
            
            future_data.append(row)
            
        df_future = pd.DataFrame(future_data)
        # Ensure column order matches training
        df_future = df_future[self.features]
        
        predictions = self.model.predict(df_future)
        return [int(max(0, p)) for p in predictions]

if __name__ == "__main__":
    # Test the training loop
    forecaster = HybridDemandForecaster()
    forecaster.train()
