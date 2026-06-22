FROM python:latest

WORKDIR /app

COPY access.log /app/access.log
COPY solution_hint.py /app/solution_hint.py
