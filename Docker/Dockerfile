FROM ubuntu:18.04

# Install Python and Qt required packages :
RUN apt-get update && apt-get install -y software-properties-common gcc && add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.6 python3-distutils python3-pip python3-apt python3-pyqt5 libgl1-mesa-glx

# Upgrade PIP to the latest version :
RUN pip3 install --upgrade pip

# Install PyQt5 :
RUN pip3 install scikit-build PyQt5

# Install PlanetarySystemStacker :
RUN pip3 install planetary-system-stacker