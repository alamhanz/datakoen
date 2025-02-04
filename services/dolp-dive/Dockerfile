# Use an official Python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app
COPY . .

# Make install.sh executable and run it
RUN chmod +x /app/install.sh && /app/install.sh

# Expose port 8001 for FastAPI
EXPOSE 8001

# Command to run the FastAPI app with Uvicorn on port 8001
CMD ["pdm", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
