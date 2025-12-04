#!/bin/bash
docker exec --tty --interactive sgbo-notebook-api .venv/bin/manage.py "$*";
