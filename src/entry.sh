#!/bin/sh

echo "start entry.sh of async_web_service"
cd src
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 8080
