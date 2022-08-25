# 3dvt Backend

This is the Backend of the 3dvt

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies

```bash
# Create a Virtual Environment
pip venv .venv

# Upgrade PIP and Wheel
pip install -U pip wheel

# On Windows
.\env\Scripts\activate

# On Linux / MacOS
source env/bin/activate

# Install All Required dependencies
pip install -r requirements.txt
```

## Starting Main Django Server

```bash
# make migrations
py manage.py makemigrations

# migrate
py manage.py migrate

# run the django server
py manage.py runserver
```

### Accessint the Backend

#### Open: [localhost:8000/api](http://localhost:8000/api) to access the DB via Django Rest Framework

### Documentation

#### Open: [localhost:8000/docs](http://localhost:8000/docs) to access the Swagger UI Documentation
