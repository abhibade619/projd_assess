#!/bin/bash

# uv pre-installed in the verifier image (tests/Dockerfile).
uvx \
  --with pytest==8.4.1 \
  pytest /tests/test_output.py -rA

if [ $? -eq 0 ]; then
  echo 1 > /app/reward.txt
else
  echo 0 > /app/reward.txt
fi
