# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
#CMD [ "python", "./app.py" ,"--host=0.0.0.0" ]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:server"]