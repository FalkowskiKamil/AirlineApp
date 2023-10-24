# Use the official Python base image with the desired version
FROM python:3.10.8


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a temporary folder and copy everything there
RUN mkdir /temp && \
    cp -r . /temp/ && \
    rm -r /temp/__pycache/ /temp/.git/

# Copy the remaining files and folders to the working directory
COPY --from=0 /temp/ .

# Expose the port that your Django app will listen on
EXPOSE 8000

# Specify the command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
