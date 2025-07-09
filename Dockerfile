FROM python:3.11-slim

# Set working directory to root
WORKDIR /

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code to root
COPY . .

# Expose port
EXPOSE 8000

# Start FastAPI explicitly from the current dir
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
