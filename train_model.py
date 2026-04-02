import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# ---------------- SAMPLE DATASET ----------------
# (You can replace with real dataset later)

data = pd.DataFrame({
    'age': [25, 45, 50, 23, 34, 65, 29, 40, 55, 60],
    'bmi': [22, 30, 28, 24, 26, 35, 23, 31, 33, 36],
    'glucose': [85, 150, 140, 90, 120, 180, 95, 160, 170, 190],
    'bp': [80, 90, 85, 70, 88, 95, 75, 92, 94, 98],
    'target': [0, 1, 1, 0, 1, 1, 0, 1, 1, 1]
})

# ---------------- FEATURES & LABEL ----------------
X = data[['age', 'bmi', 'glucose', 'bp']]
y = data['target']

# ---------------- MODEL ----------------
model = RandomForestClassifier()
model.fit(X, y)

# ---------------- SAVE MODEL ----------------
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ model.pkl created successfully!")