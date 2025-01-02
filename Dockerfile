FROM ubuntu:22.04

# Update packages index
RUN apt update

# Install Python3 and libGL required packages :
RUN apt install -y software-properties-common gcc && add-apt-repository -y ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3.12 python3-distutils python3-pip python3-apt libgl1-mesa-glx

# Upgrade PIP to the latest version :
RUN pip3 install --upgrade pip

# Install OpenCV-Python :
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-opencv

# Install tqdm :
RUN pip3 install tqdm

# Install Pillow / piexif :
RUN pip3 install Pillow piexif

# Install Wand :
RUN apt install -y libmagickwand-dev
RUN pip3 install Wand

# Install focus-stack :
RUN pip3 install focus-stack

# Install pytz :
RUN pip3 install pytz

# Install pyephem :
RUN pip3 install pyephem

# Setting up locales :
RUN apt install -y locales && locale-gen en_US.UTF-8

# Environment variables :
ENV PATH=$PATH:/opt/wolfdotsolar
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

# Copy wolfdotsolar pipeline helpers :
COPY ./src/ /opt/wolfdotsolar/