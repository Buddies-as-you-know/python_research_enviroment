# This could also be another Ubuntu or Debian based distribution
FROM ubuntu:22.04

# Set the shell to /bin/bash and enable pipefail
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Open3D system dependencies 
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential=12.9ubuntu3 \
    curl=7.85.0-1ubuntu1 \
    gcc=12-1ubuntu1 \
    libegl1=1.4.0-1 \
    libgl1=1.4.0-1 \
    libgomp1=12.3.0-1ubuntu1~22.04 \
    wget=1.21.2-2ubuntu1 \
    python3=3.10.6-1ubuntu1 \
    python3-pip=20.3.4-1ubuntu1 \
    && rm -rf /var/lib/apt/lists/*

# Size reduction by removing unnecessary things
RUN apt-get autoremove -y
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Set the path for Poetry
ENV PATH /root/.local/bin:$PATH

# Prevent Poetry from creating a virtual environment
RUN poetry config virtualenvs.create false

# Create project directory
WORKDIR /app

# Install dependencies
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

# Copy code for experimentation
COPY . .
