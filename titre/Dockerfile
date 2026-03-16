# Use Python slim image
FROM python:3.11-slim

WORKDIR /app

# Copy app and requirements
COPY titre.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Start the app
CMD ["python", "titre.py"]