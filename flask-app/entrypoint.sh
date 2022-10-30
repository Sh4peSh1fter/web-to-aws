#!/usr/bin/env bash

gunicorn --bind 0.0.0.0:${FLASK_APP_PORT} wsgi:app