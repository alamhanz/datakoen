"""_summary_

Raises:
    HTTPException: _description_

Returns:
    _type_: _description_
"""

import os

import dolphin
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

app = FastAPI()

# Predefined Secret Token (you can load this from environment variables)
SECRET_TOKEN = os.getenv("KOEN_TOKEN")

# Define API Key Header Security Scheme
api_key_header = APIKeyHeader(name="Authorization", auto_error=True)


# Authentication Dependency
def verify_token(api_key: str = Security(api_key_header)):
    """_summary_

    Args:
        api_key (str, optional): _description_. Defaults to Security(api_key_header).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    if api_key != SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")
    return api_key


@app.get("/")
def public_endpoint():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"message": "Private Access - Authentication Required"}


@app.get("/secure-data", dependencies=[Depends(verify_token)])
def protected_endpoint():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {"message": "You have access to secure data!"}


@app.get("/generate-random-slider-game", dependencies=[Depends(verify_token)])
def get_slider_data():
    """_summary_

    Example:
    To call this API, you can use the following curl command:
    ```bash
    curl -X 'GET' \
        'http://127.0.0.1:8001/generate-random-slider-game' \
        -H 'accept: application/json' \
        -H 'Authorization:test123'
    ```

    Returns:
        _type_: _description_
    """
    len_solution = 2000
    while len_solution > 800:
        slider_rl = dolphin.SliderNumber(human_render=False)
        slider_rl.auto_run()
        initial_state = slider_rl.initial_state
        slider_solution = slider_rl.steps
        len_solution = len(slider_solution)
    print(len_solution)
    return {"initial_state": initial_state.tolist(), "slider_solution": slider_solution}
