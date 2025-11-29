# Uses the official Python 3 base image as the starting environment.
FROM python:3

# Sets the working directory inside the container. All following commands run from this folder.
WORKDIR /usr/src/app

# Copies your requirements.txt file from the local machine into the container’s working directory.
COPY requirements.txt ./

# Installs the Python dependencies listed in requirements.txt directly inside the container, --no-cache-dir prevents pip from storing caches, reducing image size.
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Declares that the application inside the container listens on port 3001.
EXPOSE 3001

# Runs python server located at ./src/server.py
CMD [ "python", "./src/server.py" ]