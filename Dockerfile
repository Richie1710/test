# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script files to the container
COPY gitlab_helper.py .
COPY gitea_helper.py .
COPY main_script.py .

# Set the entry point command to execute the main script
CMD ["python", "main_script.py"]
