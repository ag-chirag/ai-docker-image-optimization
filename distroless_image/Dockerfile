# ====== BUILD STAGE ======
# Use a full Python image for building/compiling dependencies
# Match the Python version with the distroless runtime image (Python 3.11)
FROM python:3.11 AS builder

# Set the working directory for the build stage
WORKDIR /app

# Copy requirements files
COPY distroless_image/requirements.txt distroless_image/runtime_requirements.txt ./

# Install only runtime dependencies (not dev tools)
# Use --prefix to install to a separate location we can copy cleanly
RUN pip install --no-cache-dir --prefix=/pythondeps -r runtime_requirements.txt

# Copy application code for any build-time processing if needed
COPY distroless_image/app/ ./app/

# ====== RUNTIME STAGE ======
# Use Google's Distroless Python image for the final runtime
# This image contains only Python runtime, no shell, package managers, or OS utilities
FROM gcr.io/distroless/python3-debian12 AS runtime

# Set the working directory inside the container
WORKDIR /app

# In Distroless, we can't install packages, so we copy from the builder stage
# Copy ONLY the site-packages we installed, preserving the distroless launcher
# Copy to the standard location where Python looks for packages
COPY --from=builder /pythondeps/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Set PYTHONPATH so Python can find our installed packages
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages

# Copy application code and data from either the builder stage or build context
# Using build context here, but could copy from builder if there were build artifacts
COPY distroless_image/app/ ./app/
COPY distroless_image/sample_data/ ./sample_data/

# Command to run the application when the container starts.
# The distroless image has ENTRYPOINT ["python3"], so we only specify the script and args
# This avoids the duplicate python3 issue (ENTRYPOINT + CMD concatenation)
CMD ["app/predictor.py", "sample_data/sample_text.txt"]