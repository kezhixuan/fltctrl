# Base image
FROM ubuntu:22.04

# Timezone
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Berlin

# Install base tools
RUN apt update && apt -y install \
    apt-transport-https \
    sudo \
    curl

# Install python3.10
RUN apt -y install software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa

# Install odbc tools
#RUN apt-get install -y tdsodbc unixodbc-dev
#RUN apt-get install unixodbc -y
#RUN apt-get clean -y
#ADD odbcinst.ini /etc/odbcinst.ini

RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc

RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# optional: for bcp and sqlcmd
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN export PATH="$PATH:/opt/mssql-tools/bin" >> ~/.bashrc
#RUN source ~/.bashrc
# optional: for unixODBC development headers
RUN apt-get install -y unixodbc-dev
RUN apt-get install -y gettext-base 


# Setup python
ARG PYTHON_VER_MAIN=3
ARG PYTHON_VER_SUB=10
RUN apt -y install --no-install-recommends \
    # python${PYTHON_VER_MAIN}.${PYTHON_VER_SUB}-full \
    python${PYTHON_VER_MAIN}.${PYTHON_VER_SUB}-dev \
    python${PYTHON_VER_MAIN}.${PYTHON_VER_SUB}-gdbm \
    python${PYTHON_VER_MAIN}.${PYTHON_VER_SUB}-lib2to3 \
    python${PYTHON_VER_MAIN}.${PYTHON_VER_SUB}-tk \
    python${PYTHON_VER_MAIN}.${PYTHON_VER_SUB}-venv \
    python${PYTHON_VER_MAIN}.${PYTHON_VER_SUB}-distutils \
    python${PYTHON_VER_MAIN}-pip \
    python${PYTHON_VER_MAIN}-setuptools

# Install Robot Framework via pip
# debug info
RUN python3 --version 
RUN whereis python3
RUN python3 -m pip install \
    robotframework \
    ruamel.yaml \
    pyotp \
    pyodbc \
    pandas \
    sqlalchemy \
    requests \
    openpyxl \
    sshtunnel \
    seaborn \
    scikit-learn \
    numpy \
    matplotlib
    
