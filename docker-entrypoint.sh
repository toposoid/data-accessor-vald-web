#!/bin/bash

cd /app/data-accessor-vald-web
uvicorn api:app --reload --host 0.0.0.0 --port 9010
