# naive_image/Dockerfile
# This is the initial, naive Dockerfile.
# It aims to be simple and functional, but NOT optimized for size or speed.

# Use a standard, general-purpose Python image.
FROM python:3.10

RUN apt-get update && apt-get install -y curl

# Set the working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Copy requirements first for better layer caching
COPY naive_image/requirements.txt ./requirements.txt

# Install all dependencies listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and data
COPY naive_image/app/ ./app/
COPY naive_image/sample_data/ ./sample_data/

RUN echo "Build complete" > /app/build_status.txt

# Command to run the application when the container starts.
# This runs the predictor script with the sample text file.
CMD ["python", "app/predictor.py", "sample_data/sample_text.txt"]