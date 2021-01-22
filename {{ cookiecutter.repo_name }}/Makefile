.PHONY: check-safety check-style clean codestyle create-environment data download-poetry init install lint requirements sync_data_from_s3 sync_data_to_s3

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
BUCKET = {{ cookiecutter.s3_bucket }}
PROFILE = {{ cookiecutter.aws_profile }}
PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_INTERPRETER = {{ cookiecutter.python_interpreter }}

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#! An ugly hack to create individual flags
ifeq ($(STRICT), 1)
	POETRY_COMMAND_FLAG =
	PIP_COMMAND_FLAG =
	SAFETY_COMMAND_FLAG =
	BANDIT_COMMAND_FLAG =
	SECRETS_COMMAND_FLAG =
	BLACK_COMMAND_FLAG =
	DARGLINT_COMMAND_FLAG =
	ISORT_COMMAND_FLAG =
	MYPY_COMMAND_FLAG =
else
	POETRY_COMMAND_FLAG = -
	PIP_COMMAND_FLAG = -
	SAFETY_COMMAND_FLAG = -
	BANDIT_COMMAND_FLAG = -
	SECRETS_COMMAND_FLAG = -
	BLACK_COMMAND_FLAG = -
	DARGLINT_COMMAND_FLAG = -
	ISORT_COMMAND_FLAG = -
	MYPY_COMMAND_FLAG = -
endif

##! Please tell me how to use `for loops` to create variables in Makefile :(
##! If you have better idea, please PR me in https://github.com/TezRomacH/python-package-template

ifeq ($(POETRY_STRICT), 1)
	POETRY_COMMAND_FLAG =
else ifeq ($(POETRY_STRICT), 0)
	POETRY_COMMAND_FLAG = -
endif

ifeq ($(PIP_STRICT), 1)
	PIP_COMMAND_FLAG =
else ifeq ($(PIP_STRICT), 0)
	PIP_COMMAND_FLAG = -
endif

ifeq ($(SAFETY_STRICT), 1)
	SAFETY_COMMAND_FLAG =
else ifeq ($(SAFETY_STRICT), 0)
	SAFETY_COMMAND_FLAG = -
endif

ifeq ($(BANDIT_STRICT), 1)
	BANDIT_COMMAND_FLAG =
else ifeq ($(BANDIT_STRICT), 0)
	BANDIT_COMMAND_FLAG = -
endif

ifeq ($(SECRETS_STRICT), 1)
	SECRETS_COMMAND_FLAG =
else ifeq ($(SECRETS_STRICT), 0)
	SECRETS_COMMAND_FLAG = -
endif

ifeq ($(BLACK_STRICT), 1)
	BLACK_COMMAND_FLAG =
else ifeq ($(BLACK_STRICT), 0)
	BLACK_COMMAND_FLAG = -
endif

ifeq ($(DARGLINT_STRICT), 1)
	DARGLINT_COMMAND_FLAG =
else ifeq ($(DARGLINT_STRICT), 0)
	DARGLINT_COMMAND_FLAG = -
endif

ifeq ($(ISORT_STRICT), 1)
	ISORT_COMMAND_FLAG =
else ifeq ($(ISORT_STRICT), 0)
	ISORT_COMMAND_FLAG = -
endif


ifeq ($(MYPY_STRICT), 1)
	MYPY_COMMAND_FLAG =
else ifeq ($(MYPY_STRICT), 0)
	MYPY_COMMAND_FLAG = -
endif

#! The end of the ugly part. I'm really sorry

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Downloads and sets up Poetry
download-poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | $(PYTHON_INTERPRETER)

## Install Poetry dependencies
install:
	poetry lock -n
	poetry install -n
ifneq ($(NO_PRE_COMMIT), 1)
	poetry run pre-commit install
endif

## Checks type safety
check-safety:
	$(POETRY_COMMAND_FLAG)poetry check
	$(PIP_COMMAND_FLAG)poetry run pip check
	$(SAFETY_COMMAND_FLAG)poetry run safety check --full-report
	$(BANDIT_COMMAND_FLAG)poetry run bandit -ll -r {{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}/

## Checks style
check-style:
	$(BLACK_COMMAND_FLAG)poetry run black --config pyproject.toml --diff --check ./
	$(DARGLINT_COMMAND_FLAG)poetry run darglint -v 2 **/*.py
	$(ISORT_COMMAND_FLAG)poetry run isort --settings-path pyproject.toml --check-only **/*.py
	$(MYPY_COMMAND_FLAG)poetry run mypy --config-file setup.cfg {{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }} tests/**/*.py

## Checks codestyle
codestyle:
	-poetry run pyupgrade --py37-plus **/*.py
	poetry run isort --settings-path pyproject.toml **/*.py
	poetry run black --config pyproject.toml ./

## Runs tests
test:
	poetry run pytest

## Lints files
lint: test check-safety check-style

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Upload Data to S3
sync-data-to-s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(BUCKET)/data/
else
	aws s3 sync data/ s3://$(BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync-data-from-s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/data/ data/
else
	aws s3 sync s3://$(BUCKET)/data/ data/ --profile $(PROFILE)
endif

## Set up python interpreter environment
create-environment:
ifeq (True,$(HAS_CONDA))
		@echo ">>> Detected conda, creating conda environment."
ifeq (3,$(findstring 3,$(PYTHON_INTERPRETER)))
	conda create --name $(PROJECT_NAME) python={{ cookiecutter.python_version }}
else
	conda create --name $(PROJECT_NAME) python=2.7
endif
		@echo ">>> New conda env created. Activate with:\nsource activate $(PROJECT_NAME)"
		@echo ">>> Initializing git repo"
		git init
else
	$(PYTHON_INTERPRETER) -m pip install -q virtualenv virtualenvwrapper
	@echo ">>> Installing virtualenvwrapper if not already installed.\nMake sure the following lines are in shell startup file\n\
	export WORKON_HOME=$$HOME/.virtualenvs\nexport PROJECT_HOME=$$HOME/Devel\nsource /usr/local/bin/virtualenvwrapper.sh\n"
	@bash -c "source `which virtualenvwrapper.sh`;mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER)"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
endif

## Sets up repo, poetry, pre-commit hooks, and conda environment
init: download-poetry install

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Make Dataset
data:
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw data/processed


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
