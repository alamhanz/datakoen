koen:
	streamlit run home.py

build-run-mac:
	docker build --platform=linux/amd64 --build-arg TOGETHER_API_KEY="$TOGETHER_API_KEY" --build-arg hf_token="$hf_token" -t datakoen:v3 -f Dockerfile .
	docker run --name datakoenv3 -d -p 8502:8501 datakoen:v3