# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV LANGSMITH_PROJECT="enhanced-assistant-x0x-nen"
ENV LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"

# Copy the app code
COPY ./app ./app

# Expose the API port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
