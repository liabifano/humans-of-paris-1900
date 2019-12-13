REMOTE_REPO=liabifano
DOCKER_NAME=humans-of-paris
DOCKER_LABEL=latest
PROJECT_NAME=humans-of-paris
TEST_PATH=./
GIT_MASTER_HEAD_SHA:=$(shell git rev-parse --short=7 --verify HEAD)
PORT=8000
IP:=$(shell ipconfig getifaddr en0)


help:
	@echo "install - install project in dev mode using conda"
	@echo "run - run app locally"
	@echo "expose - expose ip"
	@echo "docker-build-openface - build openface docker"
	@echo "docker-run-openface - run openface docker"


docker-build:
	@docker build -t ${REMOTE_REPO}/${DOCKER_NAME}:${DOCKER_LABEL} .

docker-run:
	@docker run -it -p 8000:8000 -p 9000:9000 ${REMOTE_REPO}/${DOCKER_NAME}:${DOCKER_LABEL}

bootstrap-db:
	@bash -c "source activate humans-of-paris && \
	          export ALLOWED_HOSTS=${IP},localhost,127.0.0.1 && \
	          printf 'yes' | python humans_of_paris/manage.py reset_db && \
	          python humans_of_paris/manage.py makemigrations app && \
	          python humans_of_paris/manage.py migrate app && \
	          python humans_of_paris/manage.py runscript populate_db"


run:
	@bash -c "source activate humans-of-paris && \
	          export ALLOWED_HOSTS=${IP},localhost,127.0.0.1 && \
    	      python humans_of_paris/manage.py runserver ${IP}:${PORT}"


test: clean-pyc
	@echo "\n--- If the env $(PROJECT_NAME) doesn't exist, run 'make install' before ---\n"n
	@echo "\n--- Running tests at $(PROJECT_NAME) ---\n"
	bash -c "source activate $(PROJECT_NAME) &&  py.test --verbose --color=yes $(TEST_PATH)"


docker-build-openface:
	@echo "Don't forget to clone https://github.com/liabifano/openface"
	@bash -c "cd openface/ && docker build -t openface ."


docker-run-openface:
	@docker run -p 5000:5000 -t openface


install: clean-build clean-pyc
	-@conda env remove -yq -n $(PROJECT_NAME) # ignore if fails
	@conda create -y --name $(PROJECT_NAME) --file conda.txt
	@echo "\n --- Creating env: $(PROJECT_NAME) in $(shell which conda) ---\n"
	@echo "\n--- Installing dependencies ---\n"
	bash -c "source activate $(PROJECT_NAME) && pip install -U -r requirements.txt && conda deactivate"


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
