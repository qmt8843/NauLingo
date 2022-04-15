#!/bin/bash
exec gunicorn --certfile=cert.pem --keyfile=privkey.pem --config /app/gunicorn_config.py app.wsgi:app