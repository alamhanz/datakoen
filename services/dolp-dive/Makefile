start-service:
	uvicorn main:app --reload

build-mac:
	docker build --platform=linux/amd64 -t dolpdive:v4 -f Dockerfile .
	docker run -p 8001:8001 dolpdive:v4
