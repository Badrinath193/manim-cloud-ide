FROM mcr.microsoft.com/devcontainers/python:3.11

# Install system dependencies for Manim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-pictures \
    texlive-science \
    cm-super \
    dvipng \
    fonts-liberation \
    fonts-cmu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for headless rendering
ENV MANIM_HEADLESS=true
ENV DISPLAY=:0

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN rm /tmp/requirements.txt

# Create workspace directory
WORKDIR /workspace

# Set default shell
SHELL ["/bin/bash", "-c"]