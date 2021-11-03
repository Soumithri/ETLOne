from fastapi import FastAPI, Request
import pandas as pd
import pickle
from pydantic import BaseModel

INPUT_MODEL_FILE = 'iris_svm_model.pkl'

app = FastAPI()


class Iris(BaseModel):
    """Pydantic model for Iris dataset"""
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


def load_model(input_file):
    """Loads the ML model

    Args:
        input_file (str): Name of the model pickle file name
    """
    pkl_filename = input_file
    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)


@app.get('/')
def root():
    """GET endpoint for testing

    Returns:
        dict: message
    """
    return {'Marco': 'Polo'}


@app.post('/predict')
async def basic_predict(data: Iris):
    """POST request to predict the data from the SVM model

    Args:
        data (Iris): Iris data from sklearn

    Returns:
        int: prediction class - {0, 1, 2} for the given request
             iris data
    """
    input_df = pd.DataFrame([data.dict()])
    model = load_model(INPUT_MODEL_FILE)
    prediction = model.predict(input_df)[0]
    return prediction
