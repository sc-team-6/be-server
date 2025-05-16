# fastapi-server

Serve as the backend server for handling API requests, business logic, and database interactions using a modular and scalable architecture.

## Feature

-   Modular structure with controller - service - repository layers
-   Support for request/response data validation using DTOs (Data Transfer Objects)

## Project Structure Overview

src/
├── app.py                 # FastAPI app entrypoint
├── auth/                  # JWT-based authentication logic
├── core/                  # App-wide constants, config, and utility base classes
├── database/              # Database connection & session handling (MongoDB, Redis)
├── decorator/             # Custom decorators (e.g., logging, error handling)
├── dependencies/          # Shared dependency injection definitions
├── domain/                # Shared interfaces and business entity definitions
├── middlewares/          # Custom FastAPI middlewares (e.g., CORS, logging)
├── log/                   # Logging-related modules (e.g., saving user actions)
├── report/                # Report generation logic for analytics/statistics
├── user/                  # User management endpoints and services
└── __init__.py

## how to setup

1. brew install pipenv
2. pipenv --python 3.9
3. pipenv shell
4. DOT_ENV=development pipenv run uvicorn src.app:app --reload

## Docker (Optional)

To run with Docker Compose (MongoDB, Redis included):
1. docker-compose up --build
   
Make sure your .env file is set up correctly for development.
