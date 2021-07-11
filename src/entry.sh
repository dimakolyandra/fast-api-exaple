#!/bin/sh

echo "start entry.sh of async_web_service"
alembic upgrade head
uvicorn main:app
