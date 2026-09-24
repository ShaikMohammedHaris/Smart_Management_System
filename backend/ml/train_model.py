import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "queue_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "backend",
    "models"
)

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)


print("Loading dataset...")

data = pd.read_csv(DATASET_PATH)

print("Dataset loaded successfully!")

print("\nDataset:")
print(data)


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



y = data["waiting_time"]



X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))



model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Training completed!")


predictions = model.predict(
    X_test
)



mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)



MODEL_PATH = os.path.join(
    MODEL_DIR,
    "prediction_model.pkl"
)

joblib.dump(
    model,
    MODEL_PATH
)

