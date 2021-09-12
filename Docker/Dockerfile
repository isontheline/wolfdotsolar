FROM ubuntu:18.04

# Install Python3 and libGL required packages :
RUN apt-get update && apt-get install -y software-properties-common gcc && add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt libgl1-mesa-glx

# Upgrade PIP to the latest version :
RUN pip3 install --upgrade pip

# Install OpenCV-Python :
RUN pip3 install opencv-python opencv-python-headless

# Install tqdm :
RUN pip3 install tqdm

# Install Pillow / piexif :
RUN pip3 install Pillow piexif

# Install Wand :
RUN apt-get update && apt-get install -y libmagickwand-dev
RUN pip3 install Wand

# Install focus-stack :
RUN pip3 install focus-stack

# Setting up locales :
RUN apt-get update && apt-get install -y locales && locale-gen en_US.UTF-8

# Environment variables :
ENV PATH=$PATH:/opt/wolfdotsolar
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

# Copy wolfdotsolar pipeline helpers :
COPY ../src/ /opt/wolfdotsolar/