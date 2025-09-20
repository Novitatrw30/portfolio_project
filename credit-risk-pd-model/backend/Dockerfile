# Use lightweight Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Update pip before install
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy model into container
COPY pd_prediction_model.pkl expected_features.pkl feature_dtypes.pkl ./

# Copy app code
COPY . .

# Expose port (Cloud Run listens on $PORT)
ENV PORT=8080

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]