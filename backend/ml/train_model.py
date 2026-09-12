import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# ==========================================
# 1. FIND PROJECT DIRECTORY
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


# ==========================================
# 2. DATASET PATH
# ==========================================

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "queue_data.csv"
)


# ==========================================
# 3. MODEL DIRECTORY
# ==========================================

MODEL_DIR = os.path.join(
    BASE_DIR,
    "backend",
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


# ==========================================
# 4. LOAD DATASET
# ==========================================

print("Loading dataset...")

data = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")

print("\nDataset:")
print(data)


# ==========================================
# 5. SELECT FEATURES
# ==========================================

X = data[
    [
        "queue_length",
        "active_counters",
        "avg_service_time",
        "hour",
        "day_of_week",
        "arrival_rate"
    ]
]


# ==========================================
# 6. SELECT TARGET
# ==========================================

y = data["waiting_time"]


# ==========================================
# 7. SPLIT DATA
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# ==========================================
# 8. CREATE RANDOM FOREST MODEL
# ==========================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# ==========================================
# 9. TRAIN MODEL
# ==========================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")


# ==========================================
# 10. TEST MODEL
# ==========================================

predictions = model.predict(
    X_test
)


# ==========================================
# 11. MODEL EVALUATION
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


print("\n===================================")
print("MODEL EVALUATION")
print("===================================")

print(
    "Mean Absolute Error:",
    round(mae, 2)
)

print(
    "R2 Score:",
    round(r2, 2)
)


# ==========================================
# 12. SAVE MODEL
# ==========================================

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "prediction_model.pkl"
)

joblib.dump(
    model,
    MODEL_PATH
)


print("\n===================================")
print("MODEL TRAINING COMPLETED")
print("===================================")

print(
    "Model saved successfully!"
)

print(
    "Model location:",
    MODEL_PATH
)