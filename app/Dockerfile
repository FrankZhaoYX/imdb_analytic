# Dockerfile

# Use an official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the command to run the application
CMD ["python", "test_mysql.py"]
