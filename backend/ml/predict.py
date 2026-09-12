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

    model = joblib.load(MODEL_PATH)

    input_data = [[
        queue_length,
        active_counters,
        avg_service_time,
        hour,
        day_of_week,
        arrival_rate
    ]]

    prediction = model.predict(
        input_data
    )

    return round(
        float(prediction[0]),
        2
    )