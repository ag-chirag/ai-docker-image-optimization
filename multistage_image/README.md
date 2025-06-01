# Multi-Stage Builds for Clean AI Containers

This directory contains the **multi-stage build optimization**. This version demonstrates how to cleanly separate build-time dependencies from runtime dependencies, creating truly minimal production images.

## Purpose

This iteration shows how **multi-stage builds** use separate stages for building and running, resulting in cleaner Dockerfiles and smaller final images.

## Multi-Stage Architecture

```dockerfile
# ====== BUILD STAGE ======
FROM python:3.10 AS builder
# Install ALL dependencies (including dev tools)
# Compile any packages that need build tools

# ====== RUNTIME STAGE ======  
FROM python:3.10-slim AS runtime
# Copy only runtime requirements
# Install only runtime dependencies
# Copy application code
```

**Key Benefits:**
- **Clean Separation**: Build tools never appear in final image
- **No Cleanup Dance**: No need to install/remove build dependencies
- **Cacheable Layers**: Better Docker layer caching
- **Smaller Final Image**: Only runtime components included

## Key Optimization

**Architectural Change:**
- **Before (optimization)**: Single stage with install → build → cleanup pattern
- **After (optimization)**: Separate builder and runtime stages

**Impact:** 1.66GB → 820MB

## Usage

### Build the Image
```bash
# From the project root directory
docker build -t bert-classifier-multistage -f multistage_image/Dockerfile .
```

### Check Image Size & Layers
```bash
# View the built image and its size
docker images bert-classifier-multistage

# Expected output:
# REPOSITORY                    TAG       IMAGE ID       CREATED        SIZE
# bert-classifier-multistage    latest    <image_id>     <time_ago>     833MB

# Compare progression
docker images | grep bert-classifier | head -3
```

### Deep Dive Analysis with `dive`

Multi-stage builds create interesting layer structures:

```bash
# Analyze the multi-stage image layers
dive bert-classifier-multistage

# Compare with previous versions
dive bert-classifier-naive      # 2.54GB - shows bloated base
dive bert-classifier-slim       # 1.66GB - shows slim optimization  
dive bert-classifier-multistage # 833MB  - shows multi-stage benefits
```

**What you'll see in `dive`:**

**Multi-Stage Image Benefits:**
- Only runtime stage layers appear in final image
- No build tools or intermediate compilation artifacts
- Clean dependency separation
- Smaller total layer count in final image

**Layer Analysis:**
- Base slim layer
- Runtime Python packages only
- Application code
- **Missing**: All build tools and dev dependencies

### Run Batch Inference
```bash
# Run the default text classification
docker run --rm bert-classifier-multistage

# Expected output:s
# 
# --- Classification Result ---
# [{'label': 'POSITIVE', 'score': 0.9970954656600952}]
```

### Run as Web Server
```bash
# Start the Flask server
docker run --rm -p 8080:8080 bert-classifier-multistage python app/server.py

# Test the API
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Multi-stage builds are much cleaner!"}'
```

## ✅ What Changed 

**Dockerfile Architecture:**
1. **Added Builder Stage**: Full Python image for compilation
2. **Separate Runtime Stage**: Slim Python image for execution
3. **Dependency Split**: `requirements.txt` vs `runtime_requirements.txt`
4. **Clean Separation**: No build tools in final image

**Dependencies Refinement:**
- `runtime_requirements.txt` contains only essential runtime packages
- Removes development tools (pytest, jupyter, black, etc.)
- Keeps core ML libraries (transformers, torch, flask)