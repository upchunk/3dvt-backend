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

\*Note on Requirements:
This project use Machine Learning that require Highly Specific version off Python Module (ex: TensorFlow Windows amd64 vs TensorFlow Unix/MacOS i386). if there is any problem on installing the dependencies, please remove the package version number from the troublesome module on the requirements.txt file.

## Starting Main Django Server

```bash
# make migrations
py manage.py makemigrations

# migrate
py manage.py migrate

# run the django server
py manage.py runserver
```

### Accessing the Backend

#### Open: [localhost:8000/api](http://localhost:8000/api) to access the DB via Django Rest Framework

### Documentation

#### Open: [localhost:8000/docs](http://localhost:8000/docs) to access the Swagger UI Documentation
