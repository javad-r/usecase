import os
import argparse
import pandas as pd
from azureml.core import Run
from azureml.core.model import Model
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
import joblib

def main(args):
    # Get the current run context
    run = Run.get_context()

    # Load preprocessed data
    input_data_path = os.path.join(args.input_dir, "preprocessed_data.csv")
    df = pd.read_csv(input_data_path)
    X = df.iloc[:, :-args.num_labels].values  # Features
    Y = df.iloc[:, -args.num_labels:].values  # Labels

    # Split the data
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Train a multi-label model
    clf = MultiOutputClassifier(RandomForestClassifier()).fit(X_train, Y_train)
    
    # Evaluate the model
    accuracy = clf.score(X_test, Y_test)
    print(f"Model accuracy: {accuracy:.2f}")


    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)
    # Save the trained model
    model_path = os.path.join(args.output_dir, "dummymultilabel_classifier.pkl")
    # Save the trained model
    joblib.dump(clf, model_path)
    print(f"Model saved!")

    # Upload the model to the run
    run.upload_file(name="outputs/dummymultilabel_classifier.pkl", path_or_stream=model_path)

    # Save the vectorize and binarization for the inference
    vectorizer_path = os.path.join(args.input_dir, "vectorizer.pkl")
    mlb_path = os.path.join(args.input_dir, "label_classes.pkl")

    run.upload_file(name="outputs/vectorizer.pkl", path_or_stream=vectorizer_path)

    run.upload_file(name="outputs/label_classes.pkl", path_or_stream=mlb_path)

    # Register the model including all artifacts in Azure ML
    model = run.register_model(
        model_path="outputs/",
        model_name='multilabel_classifier', 
        properties={"accuracy": accuracy}, 
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--num_labels", type=int, required=True, help="Number of label columns")
    args = parser.parse_args()
    main(args)
