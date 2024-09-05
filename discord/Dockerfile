# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY bot /app/bot
COPY rag /app/rag

# Make sure the persist directory exists for storing vectors
RUN mkdir -p /app/persisted_vector_store
RUN mkdir -p /app/docstore

# Define environment variable
ENV PERSIST_DIR=/app/persisted_vector_store
ENV DOCSTORE_PATH=/app/docstore
ENV PYTHONPATH=/app

EXPOSE 8000

# Run the application
CMD ["python", "-m", "bot.main"]
