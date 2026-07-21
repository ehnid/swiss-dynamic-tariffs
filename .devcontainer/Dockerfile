FROM mcr.microsoft.com/devcontainers/python:3.13

RUN apt-get update && apt-get install -y \
    curl \
    git \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install \
    homeassistant \
    pillow \
    pytest \
    pytest-homeassistant-custom-component \
    ruff \
    pre-commit
