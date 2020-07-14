# Base image
FROM node:12-buster

LABEL maintainer="trinhhoangnhu@gmail.com"

# set working directory
WORKDIR /frontend

# Copy source code
COPY . /frontend

# Install dependencies
COPY ./package.json /frontend
#COPY ./package-lock.json /frontend
RUN npm install

# Build
RUN npm run build