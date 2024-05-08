#!/bin/bash

# Update and upgrade package lists
apt update && apt upgrade -y

# Install Python3 and pip if they are not installed
apt install -y python3 python3-pip

# Navigate to your project directory or clone your project
cd oneonone

# Install Python3 virtualenv if not already installed
pip3 install virtualenv

# Create a virtual environment named 'venv'
python3 -m virtualenv venv

# Activate the virtual environment
source venv/bin/activate

# Install Django, Pillow, Django REST framework, and Simple JWT
pip install Django==4.2 Pillow djangorestframework==3.14 djangorestframework-simplejwt

# Navigate to your Django project directory if not already there
cd oneonone


python manage.py makemigrations

# Run Django migrations
python manage.py migrate

echo "Setup complete."
