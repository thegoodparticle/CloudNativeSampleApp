# base image
FROM python:3.9.6-alpine3.14

# setting up a working directory inside the container
WORKDIR /app

# install system dependencies (GCC, build-base, and libffi-dev) for psutil
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    build-base \
    && rm -rf /var/lib/apt/lists/*

# install dependencies # can be part of a requirements file, for simplicity, keeping it here
RUN pip3 install --no-cache-dir fastapi uvicorn python-dotenv prometheus_client psutil

# copy the main file
COPY main.py main.py

# copy the config file - commented as k8s will fetch it from ConfigMap
# COPY ./configs /app/configs

# expose 8000 port for the application
EXPOSE 8000

# cmd to execute on container start to run the application server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
