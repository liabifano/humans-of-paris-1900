#FROM bamos/ubuntu-opencv-dlib-torch:ubuntu_14.04-opencv_2.4.11-dlib_19.0-torch_2016.07.12
FROM ubuntu:16.04

RUN ln -s /root/torch/install/bin/* /usr/local/bin

#RUN apt-get update && apt-get install -y \
#    curl \
#    git \
#    graphicsmagick \
#    libssl-dev \
#    libffi-dev \
#    python-dev \
#    python-pip \
#    python-numpy \
#    python-nose \
#    python-scipy \
#    python-pandas \
#    python-protobuf \
#    python-openssl \
#    wget \
#    zip \
#    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD openface/ /root/openface
RUN python -m pip install --upgrade --force pip
RUN cd ~/openface && \
    ./models/get-models.sh && \
    pip2 install -r /requirements.txt && \
    python2 setup.py install && \
    pip2 install --user --ignore-installed -r /demos/web/requirements.txt && \
    pip2 install -r training/requirements.txt && \
    cd ~/

# Python3
RUN apt-get update && apt-get install -y python3 python3-pip

 #CMD /bin/bash -l -c '/root/openface/demos/web/start-servers.sh'

COPY setup.py /humans-of-paris-1900/
COPY conda.txt /humans-of-paris-1900/
COPY requirements.txt /humans-of-paris-1900/
COPY src/ /humans-of-paris-1900/src/
RUN find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
RUN conda create -y --name humans-of-paris --file humans-of-paris-1900/conda.txt

#EXPOSE 8000
#CMD /bin/bash -l -c '/root/openface/demos/web/start-servers.sh'
