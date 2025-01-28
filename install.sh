#!/bin/bash

echo "apt get and req"
apt-get update
apt-get install -y $(grep -o '^[^#][[:alnum:]-]*' "apt_req.txt")
python -m pip install pip==24.2
pip install pdm==2.22.3
pdm install