#!/bin/bash

#uvicorn facebook_rss.main:api --host 0.0.0.0 --port 8000

daphne run:app -b 0.0.0.0 -p 8085
