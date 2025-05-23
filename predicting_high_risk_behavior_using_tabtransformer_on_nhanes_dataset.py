# -*- coding: utf-8 -*-
"""Predicting High-Risk Behavior Using TabTransformer on NHANES Dataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BPzItcs3lajjfbSiYl-vgafJKVwHpbfY
"""

!pip install category_encoders scikit-learn pandas torch

# https://raw.githubusercontent.com/ProjectMOSAIC/NHANES/refs/heads/master/data-raw/NHANES.csv
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import category_encoders as ce

# Load NHANES data
df = pd.read_csv("NHANES.csv")

# Drop rows with too many NaNs
df = df[['Gender', 'Age', 'Education', 'MaritalStatus', 'SexAge', 'SexNumPartnLife', 'HardDrugs']].dropna()

# Encode target
df['HardDrugs'] = df['HardDrugs'].map({'Yes': 1, 'No': 0})

# Split features
cat_cols = ['Gender', 'Education', 'MaritalStatus']
num_cols = ['Age', 'SexAge', 'SexNumPartnLife']
target_col = 'HardDrugs'

# Encode categoricals
encoder = ce.OrdinalEncoder(cols=cat_cols)
df[cat_cols] = encoder.fit_transform(df[cat_cols])

# Scale numeric features
scaler = StandardScaler()
df[num_cols] = scaler.fit_transform(df[num_cols])

# Train/test split
X = df[cat_cols + num_cols]
y = df[target_col]
X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, test_size=0.2, random_state=42)

# Torch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32).unsqueeze(1)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

class TabTransformer(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super(TabTransformer, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.attn = nn.MultiheadAttention(hidden_dim, num_heads=2, batch_first=True)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)  # [B, F] -> [B, H]
        x = x.unsqueeze(1)  # [B, H] -> [B, 1, H]
        attn_out, _ = self.attn(x, x, x)  # Self-attention
        x = attn_out.squeeze(1)  # [B, 1, H] -> [B, H]
        x = self.fc2(self.relu(x))  # [B, H] -> [B, 1]
        return self.sigmoid(x)

model = TabTransformer(input_dim=X_train.shape[1])
loss_fn = nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# Training loop
for epoch in range(20):
    model.train()
    optimizer.zero_grad()
    output = model(X_train)
    loss = loss_fn(output, y_train)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

# Save model
torch.save(model.state_dict(), "tabtransformer_model.pth")
print("✅ Model trained and saved.")

sample = pd.DataFrame([{
    'Gender': 'male',
    'Education': 'CollegeGrad',
    'MaritalStatus': 'Married',
    'Age': 25,
    'SexAge': 16,
    'SexNumPartnLife': 4
}])

# Encode and scale
sample[cat_cols] = encoder.transform(sample[cat_cols])
sample[num_cols] = scaler.transform(sample[num_cols])
input_tensor = torch.tensor(sample[cat_cols + num_cols].values, dtype=torch.float32)

# Load model and predict
model = TabTransformer(input_dim=input_tensor.shape[1])
model.load_state_dict(torch.load("tabtransformer_model.pth", map_location=torch.device('cpu')))
model.eval()

with torch.no_grad():
    prediction = model(input_tensor).item()

print(f"\n🧪 Predicted Risk Score: {prediction:.2f}")
print("⚠️ High Risk" if prediction > 0.5 else "✅ Low Risk")