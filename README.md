# Docker for AI — Lightweight, Fast, and Clean

This repository demonstrates Docker optimization techniques for AI/ML applications through practical examples and iterative improvements.

## Project Overview

This repository demonstrates how to take a simple AI inference application, a Python script using the `transformers` library and a pre-trained BERT model for text classification, and iteratively optimize its Docker containerization step-by-step.

The core application code remains stable at the top level of the repository. Each optimization technique focuses on a specific Docker optimization approach, and the corresponding subdirectory contains the `Dockerfile` (and sometimes modified requirements files) that implements that technique, building upon previous optimizations.

## Repository Structure

This repository is structured to keep core application code in a single location while demonstrating different Docker optimization approaches.

*   `naive_image/`: Contains the initial, unoptimized Docker implementation as a baseline.
*   `slim_image/`: Contains optimized Dockerfile demonstrating base image optimization.
*   `multistage_image/`: Contains Dockerfile implementing multi-stage builds.
*   `layered_image/`: Contains Dockerfile illustrating RUN command chaining and layer optimization.
*   `distroless_image/`: Contains Dockerfile using Google's distroless images for maximum security.
*   `models_image/`: Contains Dockerfile exploring model management strategies within Docker.

## Reading
1. https://www.infoq.com/articles/docker-size-dive/
2. https://dzone.com/articles/docker-image-optimization-slim-multistage
3. https://dzone.com/articles/trim-docker-images-speed-up-builds
4. https://hackernoon.com/how-to-make-docker-builds-faster-with-layer-caching
5. https://hackernoon.com/deploying-transformers-in-production-simpler-than-you-think
