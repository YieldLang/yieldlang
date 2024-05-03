#!/bin/bash

isort .
black .
ruff check .
mypy .