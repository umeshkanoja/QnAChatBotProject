# Full Stack Application

This is a full stack application with a React frontend and a Django backend.

## Table of Contents

- [Frontend](#frontend)
  - [Installation](#frontend-installation)
  - [Scripts](#frontend-scripts)
  - [Project Structure](#frontend-project-structure)
  - [Dependencies](#frontend-dependencies)
  - [Docker Setup](#frontend-docker-setup)
- [Backend](#backend)
  - [Installation](#backend-installation)
  - [Scripts](#backend-scripts)
  - [Project Structure](#backend-project-structure)
  - [Dependencies](#backend-dependencies)
  - [Docker Setup](#backend-docker-setup)

## Frontend

This is the frontend for our application, built using React and Vite.

### Frontend Installation

1. Clone the repository.
   ```bash
   git clone <repository-url>
   cd frontend- `npm run dev`: Start the development server.
- `npm run build`: Build the application for production.
- `npm run lint`: Lint the codebase.
- `npm run preview`: Preview the production build.

### Frontend Project Structure

- `src/`: Main source code directory.
  - `components/`: Reusable React components.
  - `pages/`: Page components for routing.
  - `styles/`: CSS files for styling.
  - `api.ts`: API configuration and interceptors.
- `public/`: Public assets.

### Frontend Dependencies

- React
- React DOM
- React Router DOM
- Axios
- JWT Decode

### Frontend Docker Setup

TBD

## Backend

This is the backend for our application, built using Django.

### Backend Installation

1. Create a virtual environment and activate it.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
2. Install the dependencies.
   ```bash
   pip install -r requirements.txt
   ```

### Backend Scripts

- `python manage.py runserver`: Start the development server.
- `python manage.py migrate`: Apply database migrations.
- `python manage.py makemigrations`: To generate DB migration file
- `python manage.py createsuperuser`: Create a superuser for the admin interface.

### Backend Project Structure

- `api/`: Main application directory.
  - `admin.py`: Admin configurations.
  - `apps.py`: Application configurations.
  - `models.py`: Database models.
  - `serializers.py`: Serializers for API endpoints.
  - `tests.py`: Unit tests.
  - `urls.py`: URL routing.
  - `views.py`: API views.
  - `utils/`: Utility functions and classes.
- `backend/`: Project configuration directory.
  - `settings.py`: Project settings.
  - `urls.py`: Project URL routing.
  - `wsgi.py`: WSGI configuration.
  - `asgi.py`: ASGI configuration.
- `manage.py`: Django management script.

### Backend Dependencies

- Django
- Django REST Framework

### Backend Docker Setup

TBD

## Steps to run all apps together

1. Install postgres docker using this cammand: `docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16`
1. Start postgres docker container
1. Add `.env` file in `backend` folder with following details
    ```
    DB_HOST="localhost"
    DB_PORT=6024
    DB_USER="langchain"
    DB_NAME="langchain"
    DB_PWD="langchain"

    OPENAI_API_KEY='your openai api key'
    ```
1. Generate DB migration file using `python manage.py makemigrations`
1. Perform DB migrations using `python manage.py migrate`
1. Start backend server: `python manage.py runserver`
1. Add `.env` file in `frontend` folder and add `VITE_API_URL = "http://localhost:8000"` to it.
1. Start server using: `npm run dev`
1. Open http://localhost:5173/register
1. login with newly created account
1. to logout open: http://localhost:5173/logout [TODO: Add UI to logout]