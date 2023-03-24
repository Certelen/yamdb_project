#!/bin/bash

export PYTHONPATH=/app:$PYTHONPATH

gunicorn
api_yamdb.api_yamdb.wsgi:application
--bind
0:8000