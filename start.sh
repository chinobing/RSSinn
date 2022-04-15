#!/bin/bash
#uvicorn run:app --host 0.0.0.0 --port 28085
daphne run:app -b 0.0.0.0 -p 8085
