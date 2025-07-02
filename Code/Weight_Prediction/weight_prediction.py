import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import os

# PART 1: Train the model on export.csv (training data)
print("=== TRAINING MODEL ON EXPORT.CSV ===")

# Load the training data
train_df = pd.read_csv('export.csv')

# Filter data to only include rows where filling is happening
train_df_filling = train_df[train_df['fill_level_grams_red'] > 0].copy()

# Features to use for prediction (common between export.csv and X.csv)
features = ['vibration_index_red', 'temperature_C_red', 'fill_level_grams_red']
X_train = train_df_filling[features]
y_train = train_df_filling['final_weight_grams']

# Train the model on all training data
model = LinearRegression()
model.fit(X_train, y_train)

# Get model parameters
coefs = {feature: coef for feature, coef in zip(features, model.coef_)}
intercept = model.intercept_

print(f"Model formula: y = {intercept:.2f} + ", end="")
for feature, coef in coefs.items():
    print(f"{coef:.4f} * {feature} + ", end="")
print("\b\b ")  # Remove trailing plus sign

# Make predictions on training data for evaluation
y_pred_train = model.predict(X_train)

# Evaluate the model on training data
mse = mean_squared_error(y_train, y_pred_train)
r2 = r2_score(y_train, y_pred_train)
mae = mean_absolute_error(y_train, y_pred_train)

print(f"Training Data Metrics:")
print(f"Mean Squared Error: {mse:.4f}")
print(f"R-squared: {r2:.4f}")
print(f"Mean Absolute Error: {mae:.4f}")

# Feature importance
importance = {feature: abs(coef) for feature, coef in coefs.items()}
sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
print("Feature importance:", sorted_importance)

# Visualization of model performance (training data)
plt.figure(figsize=(10, 6))
plt.scatter(y_train, y_pred_train, alpha=0.5)
plt.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], 'r--')
plt.xlabel('Actual Weight (g)')
plt.ylabel('Predicted Weight (g)')
plt.title('Model Evaluation on Training Data: Actual vs. Predicted Weight')
plt.savefig('model_evaluation_train.png')
plt.close()

# PART 2: Use the model to make predictions on X.csv
print("\n=== PREDICTING ON X.CSV ===")

# Load the test data
test_df = pd.read_csv('X.csv')
print(f"Loaded test data with {len(test_df)} rows")

# Map column names between datasets if needed
# In X.csv, temperature_C_red is called temperature_red
test_features = ['vibration_index_red', 'temperature_red', 'fill_level_grams_red']

# Filter data to only include rows where filling is happening (if applicable)
test_df_filling = test_df[test_df['fill_level_grams_red'] > 0].copy()
if len(test_df_filling) < len(test_df):
    print(f"Filtered out {len(test_df) - len(test_df_filling)} rows with zero fill level")
print(f"Making predictions on {len(test_df_filling)} rows")

# Extract features for prediction, mapping column names as needed
X_test = test_df_filling[['vibration_index_red', 'temperature_red', 'fill_level_grams_red']].copy()
X_test.rename(columns={'temperature_red': 'temperature_C_red'}, inplace=True)

# Make predictions
y_pred = model.predict(X_test)

# Create output DataFrame
output_df = pd.DataFrame({
    'ID': range(1, len(y_pred) + 1),
    'y_hat': y_pred.round(1)
})

# Save predictions to CSV
output_df.to_csv('reg_12345.csv', index=False)
print(f"Saved predictions for {len(y_pred)} samples to reg_12345.csv")

# Visualization of predictions
plt.figure(figsize=(10, 6))
plt.hist(y_pred, bins=20)
plt.xlabel('Predicted Weight (g)')
plt.ylabel('Frequency')
plt.title('Distribution of Predicted Weights')
plt.savefig('prediction_distribution.png')
plt.close()

print("\nModel training and prediction completed!")