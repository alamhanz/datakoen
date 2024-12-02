FROM python:3.11.5-bookworm
EXPOSE 8501
WORKDIR /app

COPY . .
RUN apt-get update && apt-get install -y bash
RUN chmod +x ./install.sh
RUN ls -l ./install.sh
RUN bash ./install.sh

ENTRYPOINT ["streamlit", "run", "app/home.py", "--server.port=8501", "--server.address=0.0.0.0"]