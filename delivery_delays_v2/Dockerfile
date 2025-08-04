FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update pip before install
RUN pip install --upgrade pip

# Copy both model and API code into container
COPY delivery_model_package/ ./delivery_model_package/
COPY delivery_delays_api/ ./delivery_delays_api/

# Copy model artifacts
COPY delivery_model_package/delivery_model/trained_models/ ./trained_models/
COPY delivery_model_package/delivery_model/expected_features.pkl .

# Install dependencies in one step
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose the FastAPI port
EXPOSE 8000

CMD ["uvicorn", "delivery_delays_api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]