import os

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


# ==========================================
# 1. PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET_PATH = os.path.join(BASE_DIR, "dataset", "queue_data.csv")

EXTENDED_DATASET_PATH = os.path.join(
    BASE_DIR, "dataset", "queue_data_extended.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

MODEL_PATH = os.path.join(MODEL_DIR, "prediction_model.pkl")

os.makedirs(MODEL_DIR, exist_ok=True)


FEATURES = [
    "queue_length",
    "active_counters",
    "avg_service_time",
    "hour",
    "day_of_week",
    "arrival_rate"
]


# ==========================================
# 2. LOAD ORIGINAL DATASET
# ==========================================

print("Loading original dataset...")

original = pd.read_csv(DATASET_PATH)

print("Original records:", len(original))


# ==========================================
# 3. EXTEND THE DATASET
#
# The original 30 rows only cover 2-4 counters,
# 3-5 minute service time and 2-36 people, so the
# model gave wrong answers for any other queue
# (for example 1 counter or an empty queue).
#
# In your data, waiting_time follows:
#     queue_length * avg_service_time / active_counters
# (average error about 1 minute), so we generate
# extra rows with the same pattern over a much
# wider range, with a little noise like real data.
# ==========================================

rng = np.random.default_rng(42)

ROWS = 3000

queue_length = rng.integers(0, 101, ROWS)
active_counters = rng.integers(1, 11, ROWS)
avg_service_time = rng.integers(1, 16, ROWS)
hour = rng.integers(8, 20, ROWS)
day_of_week = rng.integers(0, 7, ROWS)
arrival_rate = rng.integers(1, 16, ROWS)

base_time = queue_length * avg_service_time / active_counters

noise = rng.normal(0, 0.03, ROWS)

waiting_time = np.maximum(0, base_time * (1 + noise))

synthetic = pd.DataFrame({
    "queue_length": queue_length,
    "active_counters": active_counters,
    "avg_service_time": avg_service_time,
    "hour": hour,
    "day_of_week": day_of_week,
    "arrival_rate": arrival_rate,
    "waiting_time": np.round(waiting_time, 1)
})

data = pd.concat([original, synthetic], ignore_index=True)

data.to_csv(EXTENDED_DATASET_PATH, index=False)

print("Total training records:", len(data))


# ==========================================
# 4. HYBRID MODEL
#
# A random forest cannot learn "people x time /
# counters" well outside the values it has seen
# (an empty queue predicted 15 minutes!).
#
# So we compute that basic estimate directly, and
# the model only learns the small correction on
# top of it (busy hours, arrival rate, etc.).
# ==========================================

data["base_estimate"] = (
    data["queue_length"]
    * data["avg_service_time"]
    / data["active_counters"]
)

data["correction"] = data["waiting_time"] - data["base_estimate"]

MODEL_FEATURES = FEATURES + ["base_estimate"]

X = data[MODEL_FEATURES]

y = data["correction"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# ==========================================
# 5. TRAIN MODEL
# ==========================================

print("Training model...")

model = RandomForestRegressor(
    n_estimators=200,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ==========================================
# 6. EVALUATE (final waiting time = base + correction)
# ==========================================

base_test = X_test["base_estimate"].values

final_pred = np.maximum(0, base_test + model.predict(X_test))

final_true = base_test + y_test.values

print("\nMean Absolute Error (minutes):",
      round(mean_absolute_error(final_true, final_pred), 2))

print("R2 Score:", round(r2_score(final_true, final_pred), 4))


# ==========================================
# 7. SAVE MODEL
# ==========================================

joblib.dump(
    {
        "type": "residual",
        "model": model
    },
    MODEL_PATH
)

print("\nModel saved to:", MODEL_PATH)