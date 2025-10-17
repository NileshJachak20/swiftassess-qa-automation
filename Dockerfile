# Dockerfile for SwiftAssess QA Automation
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs

# Install K6
RUN wget -qO- https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz | tar xvz --strip-components 1 -C /usr/local/bin

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and install Node.js dependencies
COPY package.json .
RUN npm install

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p reports screenshots test_data

# Set environment variables
ENV PYTHONPATH=/app
ENV DISPLAY=:99

# Expose port for reports
EXPOSE 8080

# Default command
CMD ["pytest", "tests/", "-v", "--html=reports/test_report.html", "--self-contained-html"]
