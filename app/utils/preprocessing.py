import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_transaction(transaction):
    # Assuming transaction is a dictionary with the same structure as the training data
    df = pd.DataFrame([transaction])
    
    # Drop any columns that are not needed
    df = df.drop(columns='Time', errors='ignore')
    
    # Scale the features
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df)
    
    return scaled_df