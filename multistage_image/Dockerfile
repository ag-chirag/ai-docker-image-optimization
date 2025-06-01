# This version implements a multi-stage build to separate build-time dependencies 
# from runtime dependencies, reducing the final image size.

# ====== BUILD STAGE ======
# Use a full Python image for building/compiling dependencies
FROM python:3.10 AS builder

# Set the working directory for the build stage
WORKDIR /app

# Copy requirements files
COPY multistage_image/requirements.txt runtime_requirements.txt ./

# Install build dependencies and all packages (including dev tools)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code for any build-time processing if needed
COPY multistage_image/app/ ./app/

# ====== RUNTIME STAGE ======
# Use slim image for the final runtime
FROM python:3.10-slim AS runtime

# Set the working directory inside the container
WORKDIR /app

# Copy only the runtime requirements
COPY multistage_image/runtime_requirements.txt ./

# Install only runtime dependencies in the final image
# This excludes development tools like pytest, jupyter, etc.
RUN pip install --no-cache-dir -r runtime_requirements.txt

# Copy application code and data from either the builder stage or build context
COPY multistage_image/app/ ./app/
COPY multistage_image/sample_data/ ./sample_data/

# Command to run the application when the container starts.
CMD ["python", "app/predictor.py", "sample_data/sample_text.txt"]