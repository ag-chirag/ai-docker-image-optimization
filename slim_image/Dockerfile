# Use the slim Python image instead of the full one.
# It removes many development tools, documentation, and packages not needed for runtime.
FROM python:3.10-slim

# Set the working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

COPY slim_image/requirements.txt ./requirements.txt
COPY slim_image/app/ ./app/
COPY slim_image/sample_data/ ./sample_data/

# Install all dependencies listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application when the container starts.
CMD ["python", "app/predictor.py", "sample_data/sample_text.txt"]