# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Run Flask app
CMD ["python", "app.py"]
