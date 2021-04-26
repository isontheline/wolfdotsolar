FROM ubuntu:18.04

# Install ImageMagick :
RUN apt-get update && apt install -y imagemagick

# Install Python3 and PyQt5 required packages :
RUN apt-get update && apt-get install -y software-properties-common gcc && add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt python3-pyqt5 libgl1-mesa-glx

# Upgrade PIP to the latest version :
RUN pip3 install --upgrade pip

# Install PyQt5 :
RUN pip3 install scikit-build PyQt5

# Install PlanetarySystemStacker :
RUN pip3 install planetary-system-stacker

# Install OpenCV-Python :
RUN pip3 install opencv-python opencv-python-headless

# Install tqdm :
RUN pip3 install tqdm

# Install Pillow / piexif :
RUN pip3 install Pillow piexif

# Setting up locales :
RUN apt-get update && apt-get install -y locales && locale-gen en_US.UTF-8

# Environment variables :
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV PYTHONUNBUFFERED=1

# Copy wolfdotsolar pipeline helpers :
COPY ../src/ /opt/wolfdotsolar/