# This version demonstrates chaining RUN commands and aggressive cleanup.

# ====== BUILD STAGE ======
# Use a full Python image for building/compiling dependencies
FROM python:3.10 AS builder

# Set the working directory for the build stage
WORKDIR /app

# Copy requirements files
COPY layered_image/requirements.txt layered_image/runtime_requirements.txt ./

# Install build dependencies and all packages (including dev tools)
# The full python:3.10 image includes build tools needed for compiling packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code for any build-time processing if needed
COPY layered_image/app/ ./app/

# ====== RUNTIME STAGE ======
# Use slim image for the final runtime
FROM python:3.10-slim AS runtime

# Set the working directory inside the container
WORKDIR /app

# Copy only the runtime requirements
COPY layered_image/runtime_requirements.txt ./runtime_requirements.txt

# LAYER OPTIMIZATION: Install runtime dependencies and clean up in a single layer
# Chain commands to avoid creating intermediate layers with temporary files
# This aggressive cleanup removes caches, bytecode, and temp files, saving ~100MB
RUN pip install --no-cache-dir -r runtime_requirements.txt && \
    pip cache purge && \
    rm -rf /tmp/* /var/tmp/* && \
    find /usr/local/lib/python*/site-packages/ -name "*.pyc" -delete && \
    find /usr/local/lib/python*/site-packages/ -name "__pycache__" -type d -exec rm -rf {} + || true

# DOCKERIGNORE OPTIMIZATION: Copy application code and data
# The .dockerignore file excludes unnecessary files (docs, tests, other posts, etc.)
COPY layered_image/app/ ./app/
COPY layered_image/sample_data/ ./sample_data/

# Command to run the application when the container starts.
# This runs the predictor script with the sample text file.
CMD ["python", "app/predictor.py", "sample_data/sample_text.txt"]