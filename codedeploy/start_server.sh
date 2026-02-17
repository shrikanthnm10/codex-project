#!/usr/bin/env bash
set -euo pipefail

cat >/etc/systemd/system/erp-app.service <<'UNIT'
[Unit]
Description=ERP Flask Application
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/erp-app
Environment="DATABASE_URL=${DATABASE_URL}"
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:8000 wsgi:app
Restart=always
User=root

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable erp-app
systemctl restart erp-app
