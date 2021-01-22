#!/usr/bin/env python3

"""This module is called after project is created."""

import os
import textwrap
from pathlib import Path

# Get the root project directory:
PROJECT_DIRECTORY = Path.cwd().absolute()
PROJECT_NAME = "{{ cookiecutter.project_name }}"


def print_futher_instuctions() -> None:
    """Shows user what to do next after project creation."""
    message = f"""
    Your project {PROJECT_NAME} is created.
    1) Now you can start working on it. To create your environment:
        $ cd {PROJECT_NAME} && make create-environment && conda activate {PROJECT_NAME}
    2) Initialize git:
        $ git init
    3) Initialize poetry and install pre-commit hooks:
        $ make init
    """
    print(textwrap.dedent(message))


print_futher_instuctions()
