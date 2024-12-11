# Use a base python image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# copy the application files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 5000

# Defind the command to run the app
CMD ["python", "main.py"]