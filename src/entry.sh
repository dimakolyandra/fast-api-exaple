#!/bin/sh

alembic upgrade head
uvicorn main:app
