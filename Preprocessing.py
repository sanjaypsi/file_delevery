import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split

# List of CSV file paths
file_paths = ['path_to_first_file.csv', 'path_to_second_file.csv', 'path_to_third_file.csv']  # Update these paths as needed

# Read and concatenate all CSV files into a single DataFrame
dataframes = [pd.read_csv(file) for file in file_paths]
data = pd.concat(dataframes, ignore_index=True)

# Selecting features and labels
features = data[['Translate X', 'Translate Y', 'Translate Z', 'Rotate X', 'Rotate Y', 'Rotate Z']]
labels = data['Action']

# Encode categorical data
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Scale features
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(features)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(scaled_features, encoded_labels, test_size=0.2, random_state=42)

# Save the datasets to .npy files
np.save('X_train.npy', X_train)
np.save('X_test.npy', X_test)
np.save('y_train.npy', y_train)
np.save('y_test.npy', y_test)

# Print to confirm saving process
print("Data saved as .npy files successfully.")
