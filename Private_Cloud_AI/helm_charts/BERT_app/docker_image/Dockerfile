# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
# This allows Docker to cache the layer for dependencies,
# speeding up builds if only the application code changes.
COPY requirements.txt .

# Install the Python dependencies
# --no-cache-dir: Prevents pip from storing cached data, reducing image size.
# -r requirements.txt: Installs packages listed in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application script into the container
# The script is assumed to be named 'app.py' (or whatever you name your Python file)
COPY app.py .

# Expose the port that Gradio runs on (default is 7860)
EXPOSE 7860

# Command to run the application when the container starts
# The `python -u` flag prevents Python from buffering output,
# which is useful for seeing logs immediately in Docker.
CMD ["python", "-u", "app.py"]
