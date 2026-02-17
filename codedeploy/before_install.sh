#!/usr/bin/env bash
set -euo pipefail

yum update -y
yum install -y python3 git
python3 -m pip install --upgrade pip
python3 -m pip install -r /opt/erp-app/requirements.txt
