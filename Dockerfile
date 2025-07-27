# # Use an official lightweight Python image
# FROM python:3.11-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set work directory
# WORKDIR /app

# # Install system dependencies for PyMuPDF and spacy
# RUN apt-get update && \
#     apt-get install -y build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev && \
#     rm -rf /var/lib/apt/lists/*

# # Copy requirements and install
# COPY requirements.txt .
# RUN pip install --upgrade pip && \
#     pip install torch==2.2.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html && \
#     pip install -r requirements.txt

# # Copy the rest of the code
# COPY . .

# # Default command (can be overridden)
# CMD ["python", "analyze_collections.py"] 





# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/models

# Set work directory
WORKDIR /app

# Install system dependencies for PyMuPDF and spaCy
RUN apt-get update && \
    apt-get install -y build-essential libglib2.0-0 libsm6 libxext6 libxrender-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install torch==2.2.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html && \
    pip install -r requirements.txt

# Pre-download sentence-transformers model for offline use
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy all files into container
COPY . .

# Default command
CMD ["python", "analyze_collections.py"]
