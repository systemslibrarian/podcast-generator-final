# Use a specific, stable version of Ubuntu as the base image
# This helps ensure reproducibility and avoids unexpected changes from 'latest'.
FROM ubuntu:22.04

# Set environment variables for non-interactive apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Update apt package lists, install necessary packages, and clean up apt cache
# Combining these into a single RUN command reduces the number of Docker layers.
# python3.10 is explicitly installed.
# python3-pip for managing Python packages.
# python3-yaml for PyYAML dependency (though pip is also used for explicit PyYAML install).
# git for version control operations within the entrypoint.sh script.
RUN apt-get update && \
    apt-get install -y \
    python3.10 \
    python3-pip \
    python3-yaml \
    git && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
# All subsequent commands will run relative to this directory.
WORKDIR /app

# Copy the Python script into the container
# It's good practice to place application code in /app or similar, not /usr/bin directly.
COPY feed.py /app/feed.py

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Install Python dependencies using pip
# Using python3 -m pip install is the recommended way to invoke pip.
# Pinning the version of PyYAML for reproducibility.
RUN python3 -m pip install PyYAML==6.0.1 # Using a specific version for stability

# Define the entrypoint for the Docker container
# This script will be executed when the container starts.
ENTRYPOINT ["/app/entrypoint.sh"]

# Set the default command if no command is provided
# This is optional but can be useful for debugging or running the script directly.
# CMD ["/app/entrypoint.sh"]
