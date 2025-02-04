#!/bin/bash

echo "apt get and req"
apt-get update
apt-get install -y $(grep -o '^[^#][[:alnum:]-]*' "apt_req.txt")
rm -rf /var/lib/apt/lists/*
python -m pip install pip==25.0
pip install pdm==2.22.3
pdm install