import pandas as pd
import numpy as np

events_df = pd.read_csv('2.Raw_Events_Data.csv')
initial_rows = len(events_df)

events_df = events_df.drop_duplicates()
events_df = events_df.dropna(subset=['user_pseudo_id', 'session_id'])
events_df['session_id'] = events_df['session_id'].astype(str).str.replace('.0', '', regex=False)
events_df['price'] = events_df['price'].fillna(0)

final_rows = len(events_df)
print(f"Starting rows: {initial_rows}")
print(f"Cleaned rows: {final_rows}")
print(f"Total garbage rows removed: {initial_rows - final_rows}")


events_df['viewed_item'] = np.where(events_df['event_name'] == 'view_item', 1, 0)
events_df['added_to_cart'] = np.where(events_df['event_name'] == 'add_to_cart', 1, 0)
events_df['began_checkout'] = np.where(events_df['event_name'] == 'begin_checkout', 1, 0)
events_df['purchased'] = np.where(events_df['event_name'] == 'purchase', 1, 0)

session_data = events_df.groupby('session_id').agg({
    'viewed_item': 'sum',
    'added_to_cart': 'sum',
    'began_checkout': 'sum',
    'purchased': 'max' # 1 if they bought anything, 0 if they didn't
}).reset_index()

print(f"Total unique user sessions ready for ML: {len(session_data)}")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

print("\nTraining Random Forest Model...")

X = session_data[['viewed_item', 'added_to_cart', 'began_checkout']]
y = session_data['purchased']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

accuracy = rf_model.score(X_test, y_test) * 100
print(f"Model Accuracy: {accuracy:.2f}%")

print("Calculating Propensity Scores...")
session_data['Propensity_Score'] = rf_model.predict_proba(X)[:, 1]

session_data.to_csv('4.ML_Scored_Sessions.csv', index=False)
print("SUCCESS: '4.ML_Scored_Sessions.csv' has been created in your folder!")