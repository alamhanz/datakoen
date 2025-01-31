import dolphin
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

app = FastAPI()

# Predefined Secret Token (you can load this from environment variables)
SECRET_TOKEN = "test123"

# Define API Key Header Security Scheme
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)

slider_rl = dolphin.SliderNumber(human_render=False)
slider_rl.auto_run()
initial_state = slider_rl.initial_state
slider_solution = slider_rl.steps


# Authentication Dependency
def verify_token(api_key: str = Security(api_key_header)):
    if api_key != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")
    return api_key


@app.get("/")
def public_endpoint():
    return {"message": "Public Access - No Authentication Required"}


@app.get("/secure-data", dependencies=[Depends(verify_token)])
def protected_endpoint():
    return {"message": "You have access to secure data!"}
