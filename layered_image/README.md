# Layer Optimization - Docker Layer Surgery for AI Images

This version demonstrates how to optimize Docker layers through intelligent command chaining, cleanup operations, and layer structure improvements to minimize image bloat while maintaining full functionality.

## Purpose

This iteration focuses on **Docker layer optimization techniques** that go beyond dependency management. We chain RUN commands, implement aggressive cleanup, remove temporary files, and structure layers for maximum efficiency and caching benefits.

## 🔧 Layer Optimization Techniques

**What We Optimized:**

### 1. **Command Chaining**
```dockerfile
# Before (Multiple layers):
RUN pip install --no-cache-dir -r runtime_requirements.txt
RUN pip cache purge
RUN rm -rf /tmp/* /var/tmp/*

# After (Single optimized layer):
RUN pip install --no-cache-dir -r runtime_requirements.txt && \
    pip cache purge && \
    rm -rf /tmp/* /var/tmp/* && \
    find /usr/local/lib/python*/site-packages/ -name "*.pyc" -delete && \
    find /usr/local/lib/python*/site-packages/ -name "__pycache__" -type d -exec rm -rf {} + || true
```

### 2. **Aggressive Cleanup**
- ✅ **Pip Cache Purging**: Remove all pip download caches
- ✅ **Temporary File Removal**: Clean `/tmp/*` and `/var/tmp/*`
- ✅ **Python Bytecode**: Remove `.pyc` files and `__pycache__` directories
- ✅ **Package Caches**: Clear any remaining package manager caches

### 3. **Layer Structure Strategy**
- ✅ **Copy Requirements First**: Maximize cache hits for dependency layers
- ✅ **Install + Cleanup Together**: Prevent temporary files from persisting across layers
- ✅ **Code Copy Last**: Application changes don't invalidate dependency cache

## Key Optimization Details

**Layer Structure Analysis:**
```dockerfile
# RUNTIME STAGE Layer Breakdown:
LAYER 1: Base image (python:3.10-slim)           # ~150MB
LAYER 2: WORKDIR /app                           # ~0MB
LAYER 3: COPY runtime_requirements.txt          # ~1KB  
LAYER 4: RUN pip install + cleanup (CHAINED)    # ~570MB (optimized)
LAYER 5: COPY app/                              # ~2KB
LAYER 6: COPY sample_data/                      # ~1KB
```

**Cleanup Impact:**
```bash
# Files removed in cleanup phase:
- ~/.cache/pip/                 # Pip download cache
- /tmp/*                        # Temporary installation files  
- /var/tmp/*                    # Variable temporary files
- **/*.pyc                      # Python bytecode files
- **/__pycache__/               # Python cache directories
- Package build artifacts       # C compilation remnants
```

## 🚀 Usage

### Build the Image
```bash
# From the project root directory
docker build -t bert-classifier-layers -f layered_image/Dockerfile .
```

### Check Image Size & Layers
```bash
# View the built image and its size
docker images bert-classifier-layers

# Expected output:
# REPOSITORY                TAG       IMAGE ID       CREATED        SIZE
# bert-classifier-layers    latest    <image_id>     <time_ago>     726MB

# Inspect layer structure
docker history bert-classifier-layers
```

### Analyze Layer Efficiency with `dive`

Layer optimization shows clear improvements in structure analysis:

```bash
# Analyze the layer-optimized image
dive bert-classifier-layers

# Compare layer efficiency
dive bert-classifier-dependencies  # optimization: Multiple small layers
dive bert-classifier-layers        # optimization: Optimized layer structure
```

**What you'll see in `dive`:**

**Layer Efficiency Analysis:**
- Fewer total layers in the final image
- Single optimized dependency installation layer
- No intermediate layers with temporary files
- Better layer cache reusability
- Cleaner file structure without cache artifacts

**Key Observations:**
- Dependency layer is more efficient (single combined operation)
- No orphaned cache files visible in layer diff
- Improved layer cache hit potential for rebuilds
- Cleaner file tree structure

### Run Batch Inference
```bash
# Run the default text classification
docker run --rm bert-classifier-layers

# Expected output (functionality unchanged):
# --- Classification Result ---
# [{'label': 'POSITIVE', 'score': 0.9970954656600952}]
```

### Run as Web Server
```bash
# Start the Flask server
docker run --rm -p 8080:8080 bert-classifier-layers python app/server.py

# Test the API (all endpoints still work)
curl -X POST http://localhost:8080/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Layer optimization maintains full functionality!"}'
```

## ✅ What Changed

**Layer Structure Improvements:**
1. **Chained RUN Commands**: Combined pip install + cleanup into single layer
2. **Aggressive Cleanup**: Added comprehensive cache and temporary file removal
3. **Python Bytecode Removal**: Eliminated `.pyc` files and `__pycache__` directories
4. **Better Layer Ordering**: Optimized for maximum cache efficiency

**Build Process Optimizations:**
- Single optimized dependency installation layer
- Comprehensive cleanup prevents file accumulation
- Better rebuild performance through improved caching
- More predictable layer structure

## 🔍 Layer Optimization Methodology

**Tools for Analysis:**
```bash
# Analyze layer structure
docker history bert-classifier-layers

# Check layer sizes and commands
dive bert-classifier-layers

# Compare before/after layer efficiency
docker history bert-classifier-dependencies
docker history bert-classifier-layers

# Measure cleanup impact
docker build --no-cache -t test-cleanup -f layered_image/Dockerfile .
```

## Layer Optimization Considerations

**Benefits:**
- ✅ **Fewer Layers**: Reduced layer count improves performance
- ✅ **Better Caching**: Optimized layer structure speeds rebuilds
- ✅ **Cleaner Images**: No orphaned cache files or temporary artifacts
- ✅ **Smaller Size**: Aggressive cleanup reduces image bloat
- ✅ **Faster Builds**: Fewer layer operations and better cache hits