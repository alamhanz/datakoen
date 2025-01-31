FROM python:3.11.5-slim-bookworm

# Set environment variables
ENV TOGETHER_API_KEY=${TOGETHER_API_KEY}

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY . .

# Install dependencies and make the install script executable
RUN apt-get update && \
    apt-get install -y bash && \
    chmod +x install.sh && \
    ./install.sh

# Verify Streamlit installation
RUN pdm run streamlit --version

# Expose the port Streamlit will run on
EXPOSE 8501

# Set the entrypoint to run the Streamlit app
ENTRYPOINT ["pdm", "run", "streamlit", "run", "app/home.py", "--server.port=8501", "--server.address=0.0.0.0"]