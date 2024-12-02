import os
import argparse
import pandas as pd
from azureml.core import Run, Dataset, Datastore
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
import joblib

def main(args):
    # Get the current run context
    run = Run.get_context()
    ws = run.experiment.workspace

    # Get the input dataset
    tabular_dataset = run.input_datasets["input_data"]

    # Convert TabularDataset to pandas DataFrame
    df = tabular_dataset.to_pandas_dataframe()

    # Preprocess text (e.g., vectorization)
    vectorizer = CountVectorizer(max_features=20000)
    X = vectorizer.fit_transform(df['lemmatized_tokens']).toarray()
    feature_df = pd.DataFrame(X)

    # Binerize the labels
    mlb = MultiLabelBinarizer()
    labels = mlb.fit_transform(df['top_topics'].apply(eval)).astype('float32') 

    label_df = pd.DataFrame(labels, columns=mlb.classes_)
    output_df = pd.concat([feature_df, label_df], axis=1)
    
    # Ensure the output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    # Save preprocessed data
    output_data_path = os.path.join(args.output_dir, "preprocessed_data.csv")
    output_df.to_csv(output_data_path, index=False)


    # Save the vectorize and binarization for the inference
    vectorizer_path = os.path.join(args.output_dir, "vectorizer.pkl")
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Vectorizer saved at {vectorizer_path}")

    mlb_path = os.path.join(args.output_dir, "label_classes.pkl")
    joblib.dump(mlb, mlb_path)
    print(f"MultiLabelBinarizer saved at {mlb_path}")

    # store topic mapping
    tabular_dataset = run.input_datasets["input_data_2"] # topic mapping
    topic_df = tabular_dataset.to_pandas_dataframe()
    topic_mapping = {}
    for _, row in topic_df.iterrows():
        topic_id = int(row['topic'].split()[1])  
        keywords = row['terms'].split(",")
        topic_mapping[topic_id] = keywords
    topic_mapping_path = os.path.join(args.output_dir, "topic_mapping.pkl")
    joblib.dump(topic_mapping, topic_mapping_path)  # Serialize and save the mapping
    print(f"Topic mapping saved at {topic_mapping_path}")


    # Log artifacts to the current run
    run.log("Vectorizer Path", vectorizer_path)
    run.log("Label Binarizer Path", mlb_path)
    run.log("Topic mapping Path", topic_mapping_path)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save outputs")
    args = parser.parse_args()
    main(args)
