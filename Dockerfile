# set base image
FROM public.ecr.aws/lambda/python:3.8 AS base

# maintainer details
LABEL maintainer="Soumithri Chilakamarri <soumithri93@gmail.com>"

# copy dependencies file into working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the source directory into the working container directory
COPY src/ .

# enttry of the module to run when the container starts
CMD ["etl.handler"]