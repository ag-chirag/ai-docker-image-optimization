# app/predictor.py
import sys
import os
from transformers import pipeline

# Define the path where models are cached by default
# This is usually ~/.cache/huggingface/transformers on the host
# Inside Docker, it will be /root/.cache/huggingface/transformers
HF_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "transformers")

def get_text_classification_pipeline():
    """
    Loads a pre-trained BERT model for text classification.
    Uses the Hugging Face pipeline for simplicity.
    """
    # Using a simple pipeline for sentiment analysis as a demo
    # This will download the model weights the first time it runs
    # and cache them in HF_CACHE_DIR.
    print(f"Loading text classification pipeline. Model cache dir: {HF_CACHE_DIR}")
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    print("Model loaded.")
    return classifier

def classify_text_from_file(file_path: str):
    """
    Reads text from a file and classifies it.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    print(f"Reading text from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"Text read successfully. Length: {len(text)} characters.")
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

    if not text.strip():
        print("Warning: File is empty.")
        return "Empty input, no classification performed."

    classifier = get_text_classification_pipeline()
    print("Performing classification...")
    # The pipeline can handle a list of texts, but we'll do one for simplicity
    results = classifier(text)
    print("Classification complete.")

    return results

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app/predictor.py <path_to_text_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    # Adjust path to be relative to the /app WORKDIR in Docker
    if input_file_path.startswith('sample_data/'):
         # Assuming the script is run from /app inside docker
         # and sample_data was copied into /app
        adjusted_path = input_file_path
    else:
        # For running locally or if sample_data is not in /app in Docker
        # Let's make the Docker CMD handle the path correctly relative to WORKDIR /app
        # For local testing, the path needs to be relative to where you run the script
        print("Warning: Running locally might require adjusting input file path.")
        print("Inside Docker (WORKDIR /app), the path should be relative to /app.")
        adjusted_path = input_file_path

    classification_result = classify_text_from_file(adjusted_path)

    if classification_result:
        print("\n--- Classification Result ---")
        print(classification_result)