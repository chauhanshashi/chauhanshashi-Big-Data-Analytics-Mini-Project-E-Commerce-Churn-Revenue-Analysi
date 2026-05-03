import pandas as pd
import numpy as np
import os
import time

def generate_data(num_rows=1000000, filename="ecommerce_data.csv"):
    print(f"Generating {num_rows} rows of e-commerce data...")
    start_time = time.time()
    
    np.random.seed(42)
    
    # Generate synthetic data
    customer_ids = np.random.randint(1000, 50000, size=num_rows)
    product_ids = np.random.randint(100, 1000, size=num_rows)
    quantities = np.random.randint(1, 10, size=num_rows)
    prices = np.round(np.random.uniform(5.0, 500.0, size=num_rows), 2)
    
    # Categories: Electronics, Clothing, Home, Books, Beauty
    categories = np.random.choice(['Electronics', 'Clothing', 'Home', 'Books', 'Beauty'], size=num_rows, p=[0.25, 0.3, 0.2, 0.1, 0.15])
    
    # Dates: random dates in 2023
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', periods=num_rows).strftime('%Y-%m-%d')
    
    # Churn target (for ML): 1 if customer churns, 0 otherwise
    # Make churn slightly correlated with category and price
    churn_prob = np.where(categories == 'Electronics', 0.3, 0.1)
    churn_prob = np.where(prices > 300, churn_prob + 0.1, churn_prob)
    churn_prob = np.clip(churn_prob, 0, 1)
    churn = np.random.binomial(1, churn_prob)
    
    df = pd.DataFrame({
        'transaction_id': range(1, num_rows + 1),
        'date': dates,
        'customer_id': customer_ids,
        'product_id': product_ids,
        'category': categories,
        'quantity': quantities,
        'price': prices,
        'total_amount': quantities * prices,
        'churn': churn
    })
    
    # Save to CSV
    print(f"Saving to {filename}...")
    df.to_csv(filename, index=False)
    
    end_time = time.time()
    file_size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"Data generation complete in {end_time - start_time:.2f} seconds.")
    print(f"File created: {filename} ({file_size_mb:.2f} MB)")

if __name__ == "__main__":
    # 1 million rows will generate roughly 60-70 MB of data. 
    # For a real "Big Data" feel, you can increase this to 10,000,000 (10M rows)
    generate_data(1000000)
