FROM bamos/ubuntu-opencv-dlib-torch:ubuntu_14.04-opencv_2.4.11-dlib_19.0-torch_2016.07.12
MAINTAINER Brandon Amos <brandon.amos.cs@gmail.com>

# TODO: Should be added to opencv-dlib-torch image.
RUN ln -s /root/torch/install/bin/* /usr/local/bin

RUN apt-get update && apt-get install -y \
    curl \
    git \
    graphicsmagick \
    libssl-dev \
    libffi-dev \
    python-dev \
    python-pip \
    python-numpy \
    python-nose \
    python-scipy \
    python-pandas \
    python-protobuf \
    python-openssl \
    wget \
    zip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD . /root/openface
RUN python -m pip install --upgrade --force pip
RUN cd ~/openface && \
    ./models/get-models.sh && \
    pip2 install -r requirements.txt && \
    python2 setup.py install && \
    pip2 install --user --ignore-installed -r demos/web/requirements.txt && \
    pip2 install -r training/requirements.txt

# Python3
RUN apk upgrade --update && apk add --no-cache && \
    python3 python3-dev gcc gfortran freetype-dev musl-dev libpng-dev g++ lapack-dev

EXPOSE 8000 9000
CMD /bin/bash -l -c '/root/openface/demos/web/start-servers.sh'

#FROM continuumio/miniconda3
#
#COPY setup.py /humans-of-paris-1900/
#COPY conda.txt /humans-of-paris-1900/
#COPY requirements.txt /humans-of-paris-1900/
#COPY run-gunicorn.sh /humans-of-paris-1900/
#COPY src/ /humans-of-paris-1900/src/
#
#RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
#RUN conda create -y --name humans-of-paris --file humans-of-paris-1900/conda.txt
#RUN bash -c "cd humans-of-paris-1900 && source activate humans-of-paris && pip install . && pip install -U -r requirements.txt && conda deactivate"
#
#EXPOSE 5000
#
#WORKDIR /humans-of-paris-1900/
#CMD ["/bin/bash", "run-gunicorn.sh"]