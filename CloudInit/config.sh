#!/bin/bash


# Debug log to indicate the script has started
echo "Starting config.sh"

# Exit immediately if a command exits with a non-zero status.
set -e

# Update and upgrade packages
sudo apt update
sudo apt -y upgrade

# Install Java
sudo apt install -y openjdk-11-jre-headless

# Install Docker (commented out if not needed)
# sudo apt install -y docker.io

# Install Python 3 and pip
sudo apt install -y python3 python3-pip

# Install Pulsar Python client
pip3 install pulsar-client

# Install OpenStack clients
sudo snap install openstackclients         # For snap version (latest)
# OR
sudo apt install -y python3-openstackclient  # For APT version (specific version)
sudo apt install -y python3-novaclient python3-keystoneclient

# Install MongoDB and dependencies
sudo apt-get install -y gnupg
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" |>
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod

# Install pymongo for MongoDB interaction
pip3 install pymongo
