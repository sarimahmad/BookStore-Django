# Django Bookstore Project

This Django Bookstore project is a fully containerized web application designed for managing and purchasing books online. It leverages Django and Django REST Framework for backend operations, with Redis and Celery for task management, and PostgreSQL as the database.

## Tech Stack

- **Django**: Web framework for building robust web applications.
- **Django REST Framework**: Toolkit for building Web APIs in Django.
- **PostgreSQL**: Robust relational database system.
- **Redis**: In-memory data structure store, used as a database, cache, and message broker.
- **Celery**: Asynchronous task queue/job queue based on distributed message passing.
- **Nginx**: High-performance HTTP server and reverse proxy.

## Features

- User registration and authentication.
- CRUD operations on books, authors, and categories.
- Shopping cart functionalities.
- Automated email notifications.
- Initial data setup with fake data for books, authors, categories, and users.

## Getting Started

### Prerequisites

Ensure Docker is installed on your system. If you are unfamiliar with Docker, refer to this [Docker best practices guide](https://nickjanetakis.com/blog/best-practices-around-production-ready-web-apps-with-docker-compose).

### Clone the Repository

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/sarimahmad/BookStore-Django.git
cd BookStore-Django
```

### Configuration

1. Environment Variables:
Create a .env file in the project root directory and add the following environment variables:

```bash
DB_Name=your_database_name
DB_User=your_database_user
DB_Pass=your_database_password
```
2. Docker Setup:
This project is dockerized for easy setup and tear-down. The configurations are specified in the docker-compose.yml file.

### Configuration
Execute the following command to build and start all services:

```bash
docker-compose up --build
```

This will pull necessary Docker images, build your application images, and start the services as defined in docker-compose.yml. If you want to run it in detached mode, use the -d flag:

```bash
docker-compose up --build -d
```

### Usage
Once the application is running, you can access:

- Admin panel: http://localhost/admin
- Explore the API by navigating to http://localhost/api/ where you can interact with the endpoints defined by Django REST Framework.

#### Important Files

- docker-compose.yml: Contains all Docker service definitions.
- Dockerfile: Instructions for building the Django application Docker image.
- .env: Environment variable definitions required for Docker.
- nginx.conf: Configuration for the Nginx server that acts as a reverse proxy to handle HTTP requests.

#### Important Files

The application is configured to automatically populate the database with:

- 50 Users
- 20 Books of Every User
- 20 Authors of Every User
- 20 Categories of Every User

Superuser credentials are created automatically and can be found in the project logs