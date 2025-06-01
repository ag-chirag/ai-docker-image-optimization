# Slim Base Image Optimization

This version demonstrates how switching to a slim base image can dramatically reduce Docker image size with minimal effort.

## Purpose

This iteration shows the **single most impactful optimization** you can make: choosing the right base image. By switching from `python:3.10` to `python:3.10-slim`, we achieve a **35% size reduction** with just one line change.

## Contents

- `Dockerfile` - Optimized with slim base image
- `app/predictor.py` - Text classification inference script (unchanged)
- `app/server.py` - Flask web server for API endpoints (unchanged)
- `requirements.txt` - All dependencies including dev tools (unchanged)
- `sample_data/sample_text.txt` - Test data for classification (unchanged)

## 📊 Key Optimization

**Single Line Change:**
```dockerfile
# Before
FROM python:3.10

# After
FROM python:3.10-slim
```

**Impact:** 2.54GB → 1.66GB

## 🚀 Usage

### Build the Image
```bash
# From the project root directory
docker build -t bert-classifier-slim -f slim_image/Dockerfile .
```

### Check Image Size
```bash
# View the built image and its size
docker images bert-classifier-slim

# Expected output:
# REPOSITORY             TAG       IMAGE ID       CREATED        SIZE
# bert-classifier-slim   latest    <image_id>     <time_ago>     1.66GB

# Compare with naive version
docker images | grep bert-classifier
```

### Deep Dive Analysis with `dive`

The `dive` tool provides an excellent way to see exactly where the size savings come from:

```bash
# Analyze the naive image layers
dive bert-classifier-naive

# Analyze the slim image layers  
dive bert-classifier-slim
```

**What you'll see in `dive`:**

**Naive Image (bert-classifier-naive):**
- Large base layers from full Python image
- Includes development tools, documentation, man pages
- Many system packages you don't need for runtime

**Slim Image (bert-classifier-slim):**
- Much smaller base layers (~150MB) 
- Only essential runtime components
- Python packages are the same size (showing the optimization worked)

**Key Observations:**
- Base image difference is immediately visible in the layer breakdown
- The ML packages (transformers, torch) are identical sizes in both
- **All savings come from the base image optimization**

### Run Batch Inference
```bash
# Run the default text classification
docker run --rm bert-classifier-slim

# Expected output:
# --- Classification Result ---
# [{'label': 'POSITIVE', 'score': 0.9970954656600952}]
```

### Run as Web Server
```bash
# Start the Flask server
docker run --rm -p 8080:8080 bert-classifier-slim python slim_image/app/server.py

# Test the API
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Slim images are much smaller!"}'
```

## ✅ What Changed

**Single Optimization:**
1. **Slim Base Image**: Changed `FROM python:3.10` to `FROM python:3.10-slim`

**What's Removed:**
- Development tools (gcc, make, etc.)
- Package managers (apt-get, etc.)
- Documentation and man pages
- Unnecessary system libraries

**What's Preserved:**
- Full Python 3.10 runtime
- pip package manager
- Essential system libraries for Python packages

## ⚠️ Build Dependencies Challenge

**The Problem:**
Many AI/ML packages require compilation during installation. Slim images lack essential build tools, causing failures.

**How to Reproduce the Failure and Fix:**

### Step 1: See the Failure
```bash
# From project root directory
docker build -t bert-classifier-slim-failing -f slim_image/Dockerfile.failing .
```

This will fail with the compilation error:
```
error: command 'gcc' failed: No such file or directory
ERROR: Failed building wheel for dummy-c-extension
```

### Step 2: See the Fix
```bash
# From project root directory  
docker build -t bert-classifier-slim-fixed -f slim_image/Dockerfile.fixed .
```

This will succeed by temporarily installing build tools.

**Files for Learning:**
- `Dockerfile.failing` - Shows naive slim switch that fails
- `Dockerfile.fixed` - Shows proper build dependency management  
- `dummy_c_extension/` - Minimal C extension that guarantees compilation failure

**Common Failure Patterns:**
```
error: Failed building wheel for lxml
Building wheel for cryptography (PEP 517): FAILED  
gcc: command not found
error: cargo not found (for Rust-based packages)
```

**The Solution Pattern:**
```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libffi-dev \
    # Install packages
    && pip install --no-cache-dir -r requirements.txt \
    # Clean up in same layer
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*
```