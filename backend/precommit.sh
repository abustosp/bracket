#!/bin/bash
set -evo pipefail

black .
dmypy run -- --follow-imports=normal --junit-xml= .
ENVIRONMENT=CI pytest --cov --cov-report=xml .
pylint alembic bracket tests
isort .
