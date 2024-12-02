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
    global model, vectorizer, mlb, topic_mapping

    # Models are now available in the deployment folder
    model_dir_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'outputs')
    
    try:
        # Load the model and preprocessing objects
        model = joblib.load(os.path.join(model_dir_path, 'dummymultilabel_classifier.pkl'))
        vectorizer = joblib.load(os.path.join(model_dir_path, 'vectorizer.pkl'))
        mlb = joblib.load(os.path.join(model_dir_path, 'label_classes.pkl'))
        topic_mapping = joblib.load(os.path.join(model_dir_path, 'topic_mapping.pkl'))
        print("Model and preprocessing objects loaded successfully")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

# Function to decode predictions using topic mapping
def decode_label_predictions(predictions, topic_mapping):
    decoded_results = []
    for pred in predictions:
        decoded_topics = [topic_mapping.get(topic_id, ["Unknown"]) for topic_id in pred]
        decoded_results.append(decoded_topics)
    return decoded_results

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

        labels = mlb.inverse_transform(predictions)
        formatted_topics = [[f"topic {topic}" for topic in topic_list] for topic_list in labels]

        # Decode the predictions into human-readable topics
        decoded_terms = decode_label_predictions(labels, topic_mapping)

        # Serialize the results to JSON
        inference_results = []
        for text, pred, decoded in zip(texts, formatted_topics, decoded_terms):
            inference_results.append({
                "input_text": text,
                "predicted_topics": pred,
                "decoded_topics": decoded
            })

        # Return predictions
        return inference_results
    except Exception as e:
        return {"error": str(e)}
    