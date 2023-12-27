# Django Project README

## Overview

This Django project is designed to make web solution for users and companies.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/) (version 3.9.6)
- [PIP]() (version 23.3.2)
- [Django](https://www.djangoproject.com/) (version 4.2.8)
- [PostgreSQL](https://www.postgresql.org/) - if running manually
- [Docker](https://www.docker.com/) - if running with Docker

## Getting Started

### Running Manually

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/sat.git
    cd sat
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up PostgreSQL Database:**

    - Ensure PostgreSQL is installed.
    - Create a PostgreSQL database and user.
    - Update the `DATABASES` configuration in `main/settings.py` with your PostgreSQL credentials.

5. **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

    The application should now be accessible at [http://localhost:8000](http://localhost:8000).

### Running with Docker

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/istoickov/sat.git
    cd sat
    ```

2. **Create a `.env` File:**

    Create a `.env` file in the project root with the example content from the .env.example

3. **Build and Run Docker Containers:**

    ```bash
    docker-compose up --build
    ```

    The application should now be accessible at [http://localhost:8000](http://localhost:8000).

4. **Stop Docker Containers:**

    ```bash
    docker-compose down
    ```

### Running unit tests

There are unit test under company app that is going to testthe views:

```
python ./main/manage.py test company
```
