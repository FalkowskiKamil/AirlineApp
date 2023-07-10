# Stage 1: Build stage
FROM python:3.10.8 as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install project dependencies
RUN pip install --user -r requirements.txt

# Copy the entire Django project to the working directory
COPY . .

# Collect static files (if needed)
RUN python manage.py collectstatic --no-input


# Stage 2: Runtime stage
FROM python:3.10.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy built artifacts from the previous stage
COPY --from=builder /code /code

# Expose the port that your Django app will listen on
EXPOSE 8000

# Specify the command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
