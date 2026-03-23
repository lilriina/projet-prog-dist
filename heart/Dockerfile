FROM python:3.10
WORKDIR /app

# Copy all necessary files
COPY heart.py mysql.py heart_utils.py requirements.txt GreatVibes-Regular.ttf Quicksand-VariableFont_wght.ttf ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "heart.py"]

