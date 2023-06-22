# Ecommerce

This is a simple e-commerce project that facilitates the creation of shopping carts. Users can add products to their carts and place orders seamlessly.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have installed the latest version of Python, Django, and PostgreSQL.
* You are familiar with Python, Django, PostgreSQL, and the Django REST Framework.

## Installing Project

To install Project, follow these steps:

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

## API Endpoints

### User Endpoint

**Endpoint**: `http://127.0.0.1:8000/api/v1/register`

**Method**: `POST`

**Description**: Creates a new user upon receiving a valid POST request.


**Parameters**:

- `username`: (required) The username should be unique. Make sure to choose a username that hasn't been taken.
- `email`: (required) Please provide a valid email address.
- `password`: (required) Your password should be a minimum of 8 characters long and must include letters, numbers, and special characters for security.
- `address`: (required) Please enter your full address.
- `phone_number`: (required) Please provide your valid phone number.

**Endpoint**: `http://127.0.0.1:8000/api/v1/login`

**Method**: `POST`

**Description**: This is the login page where users can securely access their personal data.

**Parameters**:

- `username`: (required) The username should be unique. Make sure to choose a username that hasn't been taken.
- `password`: (required) Your password should be a minimum of 8 characters long and must include letters, numbers, and special characters for security.

### Products Endpoint

**Endpoint**: `http://127.0.0.1:8000/api/v1/products`

**Method**: `GET`

**Description**: This is the section where users can browse through and view details of various products.

### Cart Endpoint

**Endpoint**: `http://127.0.0.1:8000/api/v1/cart`

**Method**: `POST` | `GET` | `DELETE`

**Description**: This is the interface where you can manage your shopping cart - you can view the items in your cart, add new items, or delete existing items.


**Parameters**:

- `product`: (required) Specify the ID of the product you wish to add to or remove from your cart.

**Headers**:

- `token`: (required) Please provide your authentication token to access and modify your data.

### Order Endpoint

**Endpoint**: `http://127.0.0.1:8000/api/v1/order`

**Method**: `POST` | `GET`

**Description**: This endpoint allows you to place orders for the products in your cart and view a list of your previous orders.

**Headers**:

- `token`: (required) Please provide your authentication token to access and modify your data.

**Endpoint**: `http://127.0.0.1:8000/api/v1/order/{id}`

**Method**: `GET`

**Description**: This endpoint allows you to view the details of a specific order using its unique ID.

**Headers**:

- `token`: (required) Please provide your authentication token to access and modify your data.

