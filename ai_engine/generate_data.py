import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_historical_sales(days=365):
    """Generate dynamic synthetic sales data for training the AI model."""
    print("Generating synthetic historical sales data...")
    dates = [datetime.today() - timedelta(days=x) for x in range(days)]
    dates.reverse()

    data = []
    # Simulating 3 product categories: Silk, Cotton, Wool
    categories = ['Silk', 'Cotton', 'Wool']
    
    for date in dates:
        for category in categories:
            # Base demand
            base_demand = np.random.randint(5, 20)
            
            # Trend and Seasonality (e.g., Festival peaks in October/November)
            month = date.month
            seasonality_multiplier = 1.0
            if month in [9, 10, 11]:  # Festive season
                seasonality_multiplier = np.random.uniform(1.5, 2.5)
            elif month in [5, 6, 7]:  # Off-season
                seasonality_multiplier = np.random.uniform(0.5, 0.8)
                
            # Category specific multiplier
            cat_mult = 1.2 if category == 'Silk' else 1.0
                
            demand = int(base_demand * seasonality_multiplier * cat_mult)
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'category': category,
                'month': month,
                'day_of_week': date.weekday(),
                'is_weekend': 1 if date.weekday() >= 5 else 0,
                'demand': demand,
                'price_inr': np.random.randint(1000, 15000) if category == 'Silk' else np.random.randint(500, 5000)
            })

    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/historical_sales.csv', index=False)
    print("Data generation complete. Saved to data/historical_sales.csv")

if __name__ == "__main__":
    generate_historical_sales()
