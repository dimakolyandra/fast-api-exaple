#!/bin/sh

echo "start entry.sh of async_web_service"
pwd
ls -lsa
cd src
ls -lsa
pwd
alembic upgrade head
uvicorn main:app
