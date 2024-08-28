FROM python:3.12-slim

# Set the working directory
WORKDIR /workspace

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Entrypoint
ENTRYPOINT ["python", "-m", "src.main"]

