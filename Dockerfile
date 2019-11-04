FROM continuumio/miniconda3

COPY setup.py /humans-of-paris-1900/
COPY conda.txt /humans-of-paris-1900/
COPY requirements.txt /humans-of-paris-1900/
COPY run-gunicorn.sh /humans-of-paris-1900/
COPY src/ /humans-of-paris-1900/src/

RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
RUN conda create -y --name humans-of-paris --file humans-of-paris-1900/conda.txt
RUN bash -c "cd humans-of-paris-1900 && source activate humans-of-paris && pip install . && pip install -U -r requirements.txt && conda deactivate"

EXPOSE 5000

WORKDIR /humans-of-paris-1900/
CMD ["/bin/bash", "run-gunicorn.sh"]