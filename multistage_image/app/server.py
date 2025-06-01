# app/server.py
"""
A simple Flask server that exposes the text classification functionality via HTTP.
This is optional for the demo but useful for showcasing different deployment patterns.
"""

from flask import Flask, request, jsonify
import os
from predictor import get_text_classification_pipeline

app = Flask(__name__)

# Load the model once when the server starts
print("Initializing classifier...")
classifier = get_text_classification_pipeline()
print("Server ready!")

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy", "message": "Text classifier server is running"})

@app.route('/classify', methods=['POST'])
def classify_text():
    """
    Classify text sent via POST request.
    
    Expected JSON payload:
    {
        "text": "Your text to classify here"
    }
    
    Returns:
    {
        "result": [{"label": "POSITIVE", "score": 0.95}]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' field in request body"}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({"error": "Empty text provided"}), 400
        
        # Perform classification
        result = classifier(text)
        
        return jsonify({"result": result})
    
    except Exception as e:
        return jsonify({"error": f"Classification failed: {str(e)}"}), 500

@app.route('/classify-file', methods=['POST'])
def classify_file():
    """
    Classify text from an uploaded file.
    
    Expects a file upload with key 'file'
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Read file content
        text = file.read().decode('utf-8')
        
        if not text.strip():
            return jsonify({"error": "File is empty"}), 400
        
        # Perform classification
        result = classifier(text)
        
        return jsonify({"result": result, "filename": file.filename})
    
    except Exception as e:
        return jsonify({"error": f"File classification failed: {str(e)}"}), 500

if __name__ == '__main__':
    # Run the server
    port = int(os.environ.get('PORT', 8080))
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)