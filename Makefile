REMOTE_REPO=liabifano
DOCKER_NAME=humans-of-paris
DOCKER_LABEL=latest
PROJECT_NAME=humans-of-paris
TEST_PATH=./
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=7 --verify HEAD)


help:
	@echo "install - install project in dev mode using conda"
	@echo "run - run app locally"
	@echo "test - run tests quickly within env: $(PROJECT_NAME)"
	@echo "docker-build - build and run dockerfile"
	@echo "docker-run - run app in docker"
	@echo "docker-push - push to remove repository with commit hash attached"
	@echo "deploy-latest-pushed - deploy last version on docker hub"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove python artifacts"


docker-build:
	@docker build -t ${REMOTE_REPO}/${DOCKER_NAME}:${DOCKER_LABEL} .
	@docker run ${REMOTE_REPO}/${DOCKER_NAME}:${DOCKER_LABEL} /bin/bash -c "cd $(PROJECT_NAME); source activate $(PROJECT_NAME); py.test --verbose --color=yes $(TEST_PATH)"


docker-push:
	@docker tag ${REMOTE_REPO}/${DOCKER_NAME}:${DOCKER_LABEL} ${REMOTE_REPO}/${DOCKER_NAME}:${GIT_MASTER_HEAD_SHA}
	@echo "${DOCKER_PASSWORD}" | docker login -u="${DOCKER_USERNAME}" --password-stdin
	@docker push ${REMOTE_REPO}/${DOCKER_NAME}:${GIT_MASTER_HEAD_SHA}

docker-run:
	@docker run -p 5000:5000 ${REMOTE_REPO}/${DOCKER_NAME}:${DOCKER_LABEL}

run:
	/bin/sh run-gunicorn.sh


test: clean-pyc
	@echo "\n--- If the env $(PROJECT_NAME) doesn't exist, run 'make install' before ---\n"n
	@echo "\n--- Running tests at $(PROJECT_NAME) ---\n"
	bash -c "source activate $(PROJECT_NAME) &&  py.test --verbose --color=yes $(TEST_PATH)"


install: clean-build clean-pyc
	-@conda env remove -yq -n $(PROJECT_NAME) # ignore if fails
	@conda create -y --name $(PROJECT_NAME) --file conda.txt
	@echo "\n --- Creating env: $(PROJECT_NAME) in $(shell which conda) ---\n"
	@echo "\n--- Installing dependencies ---\n"
	bash -c "source activate $(PROJECT_NAME) && pip install -U -r requirements.txt && conda deactivate"


deploy-latest-pushed:
	bash .aws-deploy.sh


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
