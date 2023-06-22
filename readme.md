# Ecommerce

This is a simple e-commerce project that facilitates the creation of shopping carts. Users can add products to their carts and place orders seamlessly.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of Python, Django, and PostgreSQL.
* You are familiar with Python, Django, PostgreSQL, and the Django REST Framework.

## Installing YourProject

To install YourProject, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/mohamedelnadry/ecommerce
```
2. Set up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the same directory as .env.example. Copy the contents of .env.example into .env and fill in the required information.

5. Apply the database migrations:

```bash
python manage.py migrate
```


## Running YourProject
To run the server, execute:

```bash
    python manage.py runserver
```
Your application will be accessible at http://127.0.0.1:8000.
