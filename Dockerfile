# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY capstone_project/requirements.txt .
# copy rsa key
COPY id_rsa .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Start the application
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
