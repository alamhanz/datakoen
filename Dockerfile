FROM python:3.8-slim-buster
EXPOSE 8501
WORKDIR /app

COPY . .
RUN ["chmod", "+x", "./install.sh"]
RUN ./install.sh

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]