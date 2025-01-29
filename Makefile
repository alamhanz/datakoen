env:
	pip install -r requirements.txt

koen:
	streamlit run app/home.py

build-run:
	docker build -t datakoen:v3 -f Dockerfile .
	docker run --name datakoenv3 -d -p 8502:8501 datakoen:v3

launch:
	flyctl launch --auto-confirm --copy-config --dockerfile Dockerfile --name datakoen --now --org personal --region sin

fly:
	powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"