FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY bot/requirements.txt /app/
RUN pip install -r requirements.txt

# Copy bot directory and required fast_api components
COPY app/ /app/

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Run from the correct directory
CMD ["python", "main.py"]
