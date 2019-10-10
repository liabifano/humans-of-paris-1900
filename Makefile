PROJECT_NAME=humans-of-paris
TEST_PATH=./


help:
	@echo "install - install project in dev mode using conda"
	@echo "test -  run tests quickly within env: $(PROJECT_NAME)"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove python artifacts"

test: clean-pyc
	@echo "\n--- If the env $(PROJECT_NAME) doesn't exist, run 'make install' before ---\n"n
	@echo "\n--- Running tests at $(PROJECT_NAME) ---\n"
	bash -c "source activate $(PROJECT_NAME) &&  py.test --verbose --color=yes $(TEST_PATH)"


install: clean-build clean-pyc
	-@conda env remove -yq -n $(PROJECT_NAME) # ignore if fails
	@conda create -y --name $(PROJECT_NAME) --file conda.txt
	@echo "\n --- Creating env: $(PROJECT_NAME) in $(shell which conda) ---\n"
	@echo "\n--- Installing dependencies ---\n"
	bash -c "source activate $(PROJECT_NAME) && pip install -e . && pip install -U -r requirements.txt && source deactivate"


clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +


clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
