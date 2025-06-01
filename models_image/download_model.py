#!/usr/bin/env python3
"""
Script to pre-download the model during the Docker build process.
This bakes the model into the image, avoiding download time at runtime.
"""

import os
from transformers import pipeline

# Set cache directory
cache_dir = "/app/model_cache"
os.makedirs(cache_dir, exist_ok=True)

print("Pre-downloading model for baking into Docker image...")

# Download and cache the model
classifier = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english",
    cache_dir=cache_dir
)

print(f"Model successfully downloaded and cached in {cache_dir}")
print("Model will be available at runtime without internet connection.")