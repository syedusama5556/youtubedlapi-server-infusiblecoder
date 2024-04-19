# FROM python:3-alpine

# COPY ./ /app

# WORKDIR /app

# # Install git and build dependencies for certain Python packages if necessary
# # RUN apk add --no-cache git gcc musl-dev && \
# #     apk add --no-cache microdnf && \
# #     microdnf install -y gcc gcc-c++

# RUN apk add --no-cache git gcc musl-dev

# RUN pip3 install danmakuC
# RUN pip3 install --upgrade pip

# # Install dependencies
# RUN pip3 install -r requirements.txt

# EXPOSE 9191

# #ENTRYPOINT ["youtube-dl-server", "--number-processes", "1", "--host", "0.0.0.0"]
# # gunicorn -b 0.0.0.0:9191 youtubedlapi_server_infusiblecoder.app:app

# # Use CMD instead of ENTRYPOINT to easily override the command if needed
# CMD ["uvicorn", "youtubedlapi_server_infusiblecoder.app:app_asgi", "--host", "0.0.0.0", "--port", "9191", "--workers", "1", "--log-level", "info"]



# new update
# FROM almalinux:latest

# COPY ./ /app

# WORKDIR /app
# RUN dnf update -y 
# # Install git and build dependencies for certain Python packages if necessary
# RUN dnf install -y git gcc python3 python3-devel

# # Update pip
# RUN pip3 install --upgrade pip

# # Install dependencies
# RUN pip3 install -r requirements.txt

# EXPOSE 9191

# # Use CMD instead of ENTRYPOINT to easily override the command if needed
# CMD ["uvicorn", "youtubedlapi_server_infusiblecoder.app:app_asgi", "--host", "0.0.0.0", "--port", "9191", "--workers", "1", "--log-level", "info"]



# Use a base image with Python pre-installed for simplicity
FROM almalinux:latest

# Set working directory
WORKDIR /app

# Copy the application source code
COPY ./ /app

# Update system packages and install dependencies
RUN dnf update -y && \
    dnf install -y git gcc python3 python3-devel redis && \
    # Install pip and supervisord
    pip3 install --upgrade pip && \
    pip3 install supervisor

# Install application dependencies
RUN pip3 install -r requirements.txt

# Setup Supervisord
COPY supervisord.conf /etc/supervisord.conf

# Expose port 9191 for Uvicorn
EXPOSE 9191

# Configure to start supervisord on container start
CMD ["supervisord", "-c", "/etc/supervisord.conf"]
