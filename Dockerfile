# Relative path: Dockerfile

# === BASE STAGE ===
FROM python:3.9 AS base

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    autoconf \
    automake \
    libtool \
    tar \
    curl 

# Set work directory
WORKDIR /code

COPY requirements.txt /code/
RUN pip3 install --no-cache-dir -r requirements.txt

# Cleanup
RUN apt-get remove --purge -y \
    build-essential \
    autoconf \
    automake \
    libtool \
    && apt-get autoremove -y \
    && apt-get clean 


# Set work directory back to /code
WORKDIR /code

# Make port 8000 available
EXPOSE 8000

# === DEVELOPMENT STAGE ===
FROM base AS development

# Install bash-completion for development environment
RUN apt-get update && \
    apt-get install -y bash-completion && \
    rm -rf /var/lib/apt/lists/*

# Configure bash completion for development environment
RUN echo 'if [ -f /etc/bash_completion ]; then' >> /root/.bashrc && \
    echo '    . /etc/bash_completion' >> /root/.bashrc && \
    echo 'fi' >> /root/.bashrc

# Copy all necessary files and directories for development
COPY . /code/

# Define environment variable for development (you can add more if needed)
ENV NAME World

# Set the default command for development
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "flask_api:app"]

# === PRODUCTION STAGE ===
FROM base AS production

# Set permissions for the data directory
RUN chmod -R a+rw /code/data/

COPY flask_async_api.py /code/
COPY utils.py /code/

# set the time out to 120 secs
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "flask_api:app", "--timeout", "120"]