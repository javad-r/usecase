import os
import joblib
import json
import numpy as np
# from azureml.core.model import Model
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer


def init():
    global model, vectorizer, mlb

    model_dir_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'outputs')
    
    try:
        # Load the model and preprocessing objects
        model = joblib.load(os.path.join(model_dir_path, 'dummymultilabel_classifier.pkl'))
        vectorizer = joblib.load(os.path.join(model_dir_path, 'vectorizer.pkl'))
        mlb = joblib.load(os.path.join(model_dir_path, 'label_classes.pkl'))
        print("Model and preprocessing objects loaded successfully")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def run(raw_data):
    try:
        # Parse the incoming JSON data
        data = json.loads(raw_data)

        # Preprocess text: vectorize input text
        # Assume  the input JSON has a "text" key
        texts = data["text"]  
        vectorized_data = vectorizer.transform(texts).toarray()

        # Predict labels
        predictions = model.predict(vectorized_data)
        decoded_labels = mlb.inverse_transform(predictions)

        # Return predictions
        return {"predictions": decoded_labels}
    except Exception as e:
        return {"error": str(e)}