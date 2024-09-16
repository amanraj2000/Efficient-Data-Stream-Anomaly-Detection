
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY KafkaProducer.py /app/
COPY KafkaConsumer.py /app/
COPY visualize.py /app/
COPY main.py /app/

# Expose an Endpoint, 9092 is here for kafka 
EXPOSE 9092

CMD ["python", "main.py"]
