env:
	pip install -r requirements.txt

koen:
	streamlit run app/home.py

build-run:
	docker build -t datakoen:v1 -f Dockerfile .
	docker run --name datakoenv1 -d -p 8502:8501 datakoen:v1

build-to-gcp:
	gcloud builds submit --tag asia-southeast2-docker.pkg.dev/kupasdata-dev/kupasdata/kupasdata:v0.5 --timeout=2h

launch:
	flyctl launch --auto-confirm --copy-config --dockerfile Dockerfile --name datakoen --now --org personal --region sin

fly:
	powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"