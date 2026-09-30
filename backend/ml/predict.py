import os
import joblib


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "prediction_model.pkl"
)


def predict_waiting_time(
    queue_length,
    active_counters,
    avg_service_time,
    hour,
    day_of_week,
    arrival_rate
):

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Prediction model not found. "
            "Train the model first."
        )

    loaded = joblib.load(MODEL_PATH)

    features = [
        queue_length,
        active_counters,
        avg_service_time,
        hour,
        day_of_week,
        arrival_rate
    ]

    # New hybrid model: basic estimate + learned correction
    if isinstance(loaded, dict) and loaded.get("type") == "residual":

        base_estimate = (
            queue_length
            * avg_service_time
            / max(active_counters, 1)
        )

        correction = loaded["model"].predict(
            [features + [base_estimate]]
        )[0]

        prediction = max(
            0.0,
            base_estimate + float(correction)
        )

    # Old model format (still works if not retrained yet)
    else:

        prediction = float(
            loaded.predict([features])[0]
        )

    return round(prediction, 2)