#!/bin/bash
set -e

cd /home/ubuntu/webapp

# Fetch latest code
git pull origin main   # change branch if needed

# Activate venv & install deps (optional but common)
source venv/bin/activate
pip install -r requirements.txt

# Restart gunicorn service
sudo systemctl restart webapp