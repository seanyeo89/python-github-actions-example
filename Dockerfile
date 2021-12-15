# set base image (host OS)
FROM python:3.8

# Set the working directory to /app
# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# copy the content of everything/the source code to the working directory
COPY . .

# command to run on container start

CMD [ "python", "-m" , "flask", "run" , "--host=0.0.0.0" ]
