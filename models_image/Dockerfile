# This version implements a model pre-download strategy to bake models into the image,
# eliminating startup time and removing dependency on internet access at runtime.

# ====== BUILD STAGE ======
# Use a full Python image for building/compiling dependencies
FROM python:3.10 AS builder

# Set the working directory for the build stage
WORKDIR /app

# Copy requirements files
COPY models_image/requirements.txt models_image/runtime_requirements.txt ./

# Install build dependencies and all packages (including dev tools)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model download script
COPY models_image/app/ ./app/
COPY models_image/download_model.py ./

# Pre-download the model during build time
# This bakes the model weights into the Docker image
RUN python download_model.py

# ====== RUNTIME STAGE ======
# Use slim image for the final runtime
FROM python:3.10-slim AS runtime

# Set the working directory inside the container
WORKDIR /app

# Copy only the runtime requirements
COPY models_image/runtime_requirements.txt ./

# Install only runtime dependencies in the final image
# This excludes development tools like pytest, jupyter, etc.
RUN pip install --no-cache-dir -r runtime_requirements.txt

# Copy application code, data, and pre-downloaded model from builder
COPY models_image/app/ ./app/
COPY models_image/sample_data/ ./sample_data/
COPY --from=builder /app/model_cache ./model_cache

# Command to run the application when the container starts.
CMD ["python", "app/predictor.py", "sample_data/sample_text.txt"]