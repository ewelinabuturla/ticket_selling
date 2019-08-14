FROM python:3.6-slim

# Set environment variables
# Do not write .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure that Python outputs everything that's printed inside. 
# the application rather than buffering it, maily for logging purposes
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install all necessary dependencies
RUN pip install pipenv
COPY Pipfile* /app/
RUN pipenv install --system

# Copy app
COPY . /app/
