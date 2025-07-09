# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything (yes, everything)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["python3", "app.py"]
