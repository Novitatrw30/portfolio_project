FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

# Update pip before install
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["streamlit", "run", "app_frontend.py", "--server.port=8080", "--server.address=0.0.0.0"]