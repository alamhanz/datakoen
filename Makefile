kupas:
	streamlit run app/Home.py

build-run:
	docker build -t pealtest:v1 -f Dockerfile .
	docker run --name pealv1 -d -p 8502:8501 pealtest:v1

build-to-gcp:
	gcloud builds submit --tag asia-southeast2-docker.pkg.dev/kupasdata-dev/kupasdata/kupasdata:v0.5 --timeout=2h