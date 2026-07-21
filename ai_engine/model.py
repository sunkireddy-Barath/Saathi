import pandas as pd
import numpy as np
import xgboost as xgb
from prophet import Prophet
from sklearn.metrics import mean_squared_error
import joblib
import os

class HybridDemandForecaster:
    def __init__(self):
        self.macro_model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False)
        self.micro_model = xgb.XGBRegressor(
            objective='reg:squarederror', 
            n_estimators=100, 
            learning_rate=0.1, 
            max_depth=5
        )
        self.is_trained = False
        self.alpha = 0.6  # Decay factor for micro-fads
        self.confidence_score = 0.0

    def apply_exponential_decay(self, series, alpha):
        """Applies exponential smoothing decay to a series."""
        return series.ewm(alpha=alpha, adjust=False).mean()

    def train(self, data_path='data/historical_sales.csv'):
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file {data_path} not found. Run generate_data.py first.")
            
        print("Loading training data for Sequential Residual Learning...")
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        
        # Step 1: Train Macro Model (Prophet)
        prophet_df = df[['date', 'demand']].rename(columns={'date': 'ds', 'demand': 'y'})
        self.macro_model.fit(prophet_df)
        
        # Predict baseline on training data to get residuals
        forecast = self.macro_model.predict(prophet_df[['ds']])
        df['prophet_baseline'] = forecast['yhat'].values
        
        # Calculate residuals (e = y - y_hat)
        df['residual'] = df['demand'] - df['prophet_baseline']
        
        # Step 2: Apply Exponential Decay to micro-metrics
        df = df.sort_values('date')
        df['clicks_decayed'] = self.apply_exponential_decay(df['clicks'], self.alpha)
        df['search_volume_decayed'] = self.apply_exponential_decay(df['search_volume'], self.alpha)
        df['item_views_decayed'] = self.apply_exponential_decay(df['item_views'], self.alpha)
        
        # Feature Engineering for Micro Model
        df = pd.get_dummies(df, columns=['category'], drop_first=True)
        self.features = [col for col in df.columns if col.startswith('category_') or col in [
            'clicks_decayed', 'search_volume_decayed', 'item_views_decayed', 'month', 'day_of_week', 'is_weekend'
        ]]
        
        # Fill missing dummy columns if a category wasn't in the dataset
        for f in self.features:
            if f not in df.columns:
                df[f] = 0
                
        X = df[self.features]
        y_res = df['residual']
        
        # Step 3: Train Micro Model (XGBoost) on residuals
        print("Training XGBoost on residuals...")
        self.micro_model.fit(X, y_res)
        
        # Calculate real Confidence Score
        preds_res = self.micro_model.predict(X)
        final_preds = df['prophet_baseline'] + preds_res
        
        rmse = np.sqrt(mean_squared_error(df['demand'], final_preds))
        mean_demand = df['demand'].mean()
        
        error_ratio = rmse / (mean_demand + 1e-5)
        self.confidence_score = max(0.0, min(1.0, 1.0 - error_ratio))
        print(f"Model trained. RMSE: {rmse:.2f}, Confidence Score: {self.confidence_score*100:.1f}%")
        
        # Save artifacts
        os.makedirs('models', exist_ok=True)
        joblib.dump({
            'macro_model': self.macro_model, 
            'micro_model': self.micro_model, 
            'features': self.features,
            'confidence_score': self.confidence_score
        }, 'models/hybrid_forecaster.pkl')
        self.is_trained = True

    def load_model(self):
        if os.path.exists('models/hybrid_forecaster.pkl'):
            artifact = joblib.load('models/hybrid_forecaster.pkl')
            self.macro_model = artifact['macro_model']
            self.micro_model = artifact['micro_model']
            self.features = artifact['features']
            self.confidence_score = artifact.get('confidence_score', 0.85)
            self.is_trained = True
        else:
            raise FileNotFoundError("Model file not found. Train the model first.")

    def predict_next_n_days(self, category: str, n_days: int = 30):
        if not self.is_trained:
            self.load_model()
            
        from datetime import datetime, timedelta
        base_date = datetime.today()
        
        # 1. Macro prediction
        future_dates = [base_date + timedelta(days=i) for i in range(1, n_days + 1)]
        future_prophet = pd.DataFrame({'ds': future_dates})
        macro_forecast = self.macro_model.predict(future_prophet)
        baseline_preds = macro_forecast['yhat'].values
        
        # 2. Micro features prediction
        future_data = []
        for i, dt in enumerate(future_dates):
            row = {
                'month': dt.month,
                'day_of_week': dt.weekday(),
                'is_weekend': 1 if dt.weekday() >= 5 else 0,
                'clicks_decayed': 10,
                'search_volume_decayed': 50,
                'item_views_decayed': 100,
            }
            for feat in self.features:
                if feat.startswith('category_'):
                    row[feat] = 1 if feat == f'category_{category}' else 0
            future_data.append(row)
            
        df_future_micro = pd.DataFrame(future_data)[self.features]
        
        # 3. Micro prediction (Residuals)
        micro_res_preds = self.micro_model.predict(df_future_micro)
        
        # 4. Final Combination
        final_predictions = baseline_preds + micro_res_preds
        return [int(max(0, p)) for p in final_predictions], self.confidence_score

if __name__ == "__main__":
    forecaster = HybridDemandForecaster()
    forecaster.train()
