# JouerFlux

JouerFlux is a Flask-based application designed to manage firewalls, filtering policies, and firewall rules. It utilizes SQLite as the database and exposes a RESTful API for managing these entities. The application includes Swagger documentation for easy API testing.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)

## Continuous Integration

This project includes continuous integration (CI) to automate testing and ensure code quality. Each new commit triggers automated testing using a CI pipeline, which runs `pytest` to verify the application's integrity.

## Features

- Add, display, and delete firewalls.
- Add, display, and delete filtering policies for each firewall.
- Add, display, and delete firewall rules for each filtering policy.
- Comprehensive Swagger documentation for API testing.

## Architecture

The application follows a modular structure:

```
/app
    ├── __init__.py
    ├── models
    │   ├── __init__.py
    │   ├── firewall.py
    │   ├── policy.py
    │   ├── rule.py
    │   └── user.py
    ├── routes
    │   ├── firewall_route.py
    │   ├── policy_route.py
    │   ├── rule_route.py
    │   └── user_route.py
    ├── schemas
    │   ├── __init__.py
    │   ├── firewall_schema.py
    │   ├── policy_schema.py
    │   ├── rule_schema.py
    │   └── user_schema.py
    ├── services
    │   ├── firewall_service.py
    │   ├── policy_service.py
    │   ├── rule_service.py
    │   └── user_service.py
    └── utils
        └── decorators.py
/tests
    ├── __init__.py
    ├── test_firewall.py
    ├── test_policy.py
    └── test_rule.py
.env                  # Environment variables
config.py            # Configuration settings
docker-compose.yml    # Docker Compose configuration
Dockerfile            # Dockerfile for building the image
run.py               # Entry point for running the application
```

### Prerequisites

Ensure that you have Python 3.9 and `pip` installed on your system.

1. Clone the repository:
    ```
    git clone https://github.com/Yannick-N/jouer-flux.git
    cd jouer-flux
    ```

2. Install Flask and other dependencies:
    ```
    pip install -r requirements.txt
    ```

## Running the Application

1. Build and run the Docker images:
    ```
    docker-compose build
    docker-compose up
    ```

2. Access the Swagger documentation at [http://127.0.0.1:8080/apidocs](http://127.0.0.1:8080/apidocs).

3.	API Authentication: 

In the user API, there is a default admin user available for login. To authenticate and obtain an access token, send a login request to the `/api/v1/users/login` endpoint with the default admin credentials. Once you receive the access token, you can use it to authorize your API requests.

To use the token in the Swagger UI, click on the “Authorize” button located in the top right corner. In the input field, WRITE `Bearer {token}`. This will grant you access to the protected API endpoints.

## Running Tests

To run tests, use `pytest`:

1. Install `pytest` if it's not already installed:
    ```
    pip install pytest
    ```

2. Run the tests:
    ```
    pytest
    ```

This will execute all the unit tests in the `/tests` directory, ensuring that each component of the application is working correctly.

## API Endpoints

Here are the main API endpoints:

### Firewalls
- **GET** `/api/v1/firewalls/` - Retrieve a list of all firewalls.
- **POST** `/api/v1/firewalls/` - Create a new firewall.
- **DELETE** `/api/v1/firewalls/{id}` - Delete a firewall by ID.
- **GET** `/api/v1/firewalls/{id}` - Get a specific firewall by ID.
- **PUT** `/api/v1/firewalls/{id}` - Update a firewall by ID.

### Policies
- **GET** `/api/v1/firewalls/{firewall_id}/policies` - Retrieve all policies for a specific firewall.
- **POST** `/api/v1/firewalls/{firewall_id}/policies` - Create a new policy for a firewall.
- **DELETE** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}` - Delete a specific policy for a firewall.
- **GET** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}` - Retrieve a specific policy by ID for a given firewall.
- **PUT** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}` - Update an existing policy for a firewall.

### Rules
- **GET** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}/rules` - Retrieve all rules for a specific policy under a given firewall.
- **POST** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}/rules` - Create a new rule for a policy under a specific firewall.
- **DELETE** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}/rules/{rule_id}` - Delete a specific rule for a policy under a specific firewall.
- **GET** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}/rules/{rule_id}` - Retrieve a specific rule by ID for a given policy and firewall.
- **PUT** `/api/v1/firewalls/{firewall_id}/policies/{policy_id}/rules/{rule_id}` - Update an existing rule for a policy under a specific firewall.

### Users
- **POST** `/api/v1/users/login` - Login user and retrieve an access token.
- **POST** `/api/v1/users/register` - Register a new user.
- **DELETE** `/api/v1/users/{id}` - Delete a user by ID.
- **GET** `/api/v1/users/{id}` - Get a user by ID.
- **PUT** `/api/v1/users/{id}` - Update a user by ID.