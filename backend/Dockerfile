# --- Stage 1: Build with full tools ---
FROM python:3.12-slim AS builder

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install build tools and copy requirements
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential

COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .


# --- Stage 2: Minimal runtime ---
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy only installed packages and app
COPY --from=builder /install /usr/local
COPY --from=builder /app /app

CMD ["python3", "main.py"]
