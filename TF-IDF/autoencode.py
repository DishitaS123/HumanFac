import pandas as pd
import numpy as np
import tensorflow as tf
import ast
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from sklearn.preprocessing import MinMaxScaler

# === Load CSV Data ===
csv_file = "input_data/Vectorized_Traslated_BERT_Output.csv"  # Change this to your actual file
df = pd.read_csv(csv_file)

# === Extract Features (Skipping ID Column) ===
X = df.iloc[:, 1].apply(lambda x: np.array(ast.literal_eval(x))).values
X = np.vstack(X)  # Stack the arrays into a 2D array

# === Normalize Data (Optional but Recommended) ===
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# === Define Autoencoder Architecture ===
input_dim = X_scaled.shape[1]  # Number of features
encoding_dim = 64  # Size of compressed representation (adjust as needed)

# Encoder
input_layer = Input(shape=(input_dim,))
encoded = Dense(128, activation="relu")(input_layer)
encoded = Dense(encoding_dim, activation="relu")(encoded)  # Bottleneck layer

# Decoder
decoded = Dense(128, activation="relu")(encoded)
decoded = Dense(input_dim, activation="sigmoid")(decoded)  # Sigmoid for normalized output

# === Build Autoencoder Model ===
autoencoder = Model(input_layer, decoded)
autoencoder.compile(optimizer="adam", loss="mse")

# === Train Autoencoder ===
autoencoder.fit(X_scaled, X_scaled, epochs=50, batch_size=32, shuffle=True, validation_split=0.1)

# === Extract Encoder Model ===
encoder = Model(input_layer, encoded)

# === Encode the Data ===
X_encoded = encoder.predict(X_scaled)

# === Save Encoded Data to CSV ===
encoded_df = pd.DataFrame(X_encoded)
encoded_df.insert(0, "ID", df.iloc[:, 0])  # Re-add the ID column
encoded_df.to_csv("encoded_data.csv", index=False)

print("Autoencoding complete! Encoded data saved to 'encoded_data.csv'.")
