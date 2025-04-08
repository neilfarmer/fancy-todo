# Use an official Python 3.13 image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Copy project files
COPY . .

# Install dependencies via Poetry
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --no-root

# Expose port
EXPOSE 5001

# Set environment variable for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Run the Flask app
CMD ["poetry", "run", "flask", "run", "--port=5001"]