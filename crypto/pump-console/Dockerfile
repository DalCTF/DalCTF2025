# Use a minimal, secure base image with Python
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set a working directory
WORKDIR /app

# Copy the application files
COPY app.py .
COPY templates/ ./templates/
COPY flag.txt .

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make the script executable
RUN chmod +x app.py

# Create an unprivileged user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Keep everything owned by root, but make it readable by appuser
RUN chmod -R 755 /app && \
    chmod 444 /app/flag.txt && \
    # Make templates directory readable by appuser
    chmod -R 755 /app/templates && \
    # Make app.py executable by appuser but still owned by root
    chmod 755 /app/app.py

# Expose the port the challenge will run on
EXPOSE 1337

# Run the Flask application as unprivileged user
USER appuser
CMD ["gunicorn", "--bind", "0.0.0.0:1337", "app:app"]
