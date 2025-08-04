# Stage 1: Builder
FROM python:3.13-slim AS builder

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry
WORKDIR /app
COPY . .
RUN poetry build -f wheel -n
LABEL authors="Segelzwerg"

# Stage 2: Runtime
FROM python:3.13-slim
WORKDIR /app
COPY --from=builder /app/dist/ .
COPY entrypoint.sh .
RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --find-links . portauthority
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]