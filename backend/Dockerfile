# Base image
FROM python:3.7-buster

LABEL maintainer="trinhhoangnhu@gmail.com"

# set working directory
WORKDIR /backend

# Copy source code
COPY . /backend

# Install dependencies
RUN pip install -r requirement.txt
