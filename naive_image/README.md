# Naive Docker Implementation

This directory contains the **baseline naive Docker implementation**. This version prioritizes simplicity and functionality over optimization.

## Purpose

This is the starting point that demonstrates a working but unoptimized Docker setup for ML inference. It serves as the baseline to measure improvements against in other optimizations.

## Contents

- `Dockerfile` - Simple, unoptimized Docker configuration
- `app/predictor.py` - Text classification inference script
- `app/server.py` - Flask web server for API endpoints
- `requirements.txt` - All dependencies including dev tools
- `sample_data/sample_text.txt` - Test data for classification

## Usage

### Build the Image
```bash
# From the project root directory
docker build -t bert-classifier-naive -f naive_image/Dockerfile .
```

### Check Image Size
```bash
# View the built image and its size
docker images bert-classifier-naive

# Expected output:
# REPOSITORY              TAG       IMAGE ID       CREATED        SIZE
# bert-classifier-naive   latest    <image_id>     <time_ago>     2.54GB
```

### Run Batch Inference
```bash
# Run the default text classification
docker run --rm bert-classifier-naive

# Expected output:
# --- Classification Result ---
# [{'label': 'POSITIVE', 'score': 0.9970954656600952}]
```

### Run as Web Server
```bash
# Start the Flask server
docker run --rm -p 8080:8080 bert-classifier-naive python app/server.py

# Test the API
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Docker makes ML deployment so much easier!"}'
```

## 🐳 Known Inefficiencies

This naive implementation has several optimization opportunities that will be addressed in later optimizations:

1. **Large Base Image**: Uses full Python image instead of slim
2. **Bloated Dependencies**: Includes dev tools not needed for runtime
3. **Poor Layer Caching**: Single RUN command hurts Docker layer caching
4. **Large Build Context**: Copies unnecessary files
5. **No Multi-stage Build**: Doesn't separate build and runtime environments