FROM python:3.9-slim

WORKDIR /app

COPY . .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and switch to it
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["python", "app.py"]
