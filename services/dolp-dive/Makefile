start-service:
	uvicorn main:app --reload

build-mac:
	echo "KOEN_TOKEN=$(KOEN_TOKEN)"
	docker build --platform=linux/amd64 -t dolpdive:v4 -f Dockerfile .
	docker run -p 8001:8001 -e KOEN_TOKEN=$(KOEN_TOKEN) dolpdive:v4
