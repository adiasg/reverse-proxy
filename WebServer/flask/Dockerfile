# Use an official Ubuntu as a parent image
FROM ubuntu:17.10

RUN apt-get update

RUN apt-get install -y python3-pip python3-dev

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir --requirement requirements.txt

RUN apt-get install -y uwsgi uwsgi-plugin-python3

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
ENTRYPOINT ["/bin/bash"]
CMD ["run.sh"]
