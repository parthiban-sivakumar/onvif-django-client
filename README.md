# onvif-python
Onvif django app for viewing camera device information, system date time, and system logs.

## Requirements

- Python 3.10+
- Django 5.2.5
- Other dependencies: see `requirements.txt`

## Installation:

`pip install django`  
`pip install --upgrade onvif_zeep`

## Initial Setup

After cloning the repository and installing dependencies, set up the database:

# Generate migration files
python manage.py makemigrations

# Apply migrations to create tables
python manage.py migrate


## Update

Got the finalist prize of Onvif Spotlight challenge for creating this app.

 My submission : https://onvif-spotlight.bemyapp.com/#/projects/5b13e8c6b4e28a000442fb94
 
 Prize announcement : https://www.onvif.org/blog/2018/07/onvif-challenge-announces-top-10/
