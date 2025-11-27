# Bengaluru Vendor-Event Discovery Web App

A full-stack web application for discovering and clustering events in Bengaluru to recommend them to vendors using geospatial clustering.

## Tech Stack
- **Frontend**: Vue 3, Vite, Pinia, TailwindCSS, Mapbox GL JS
- **Backend**: FastAPI, SQLModel, AsyncPG, Celery
- **Database**: PostgreSQL + PostGIS
- **ML/Clustering**: Python (scikit-learn, DBSCAN)
- **Infrastructure**: Docker Compose

## Prerequisites
- Docker & Docker Compose installed and running.
- Mapbox Access Token (for frontend map).

## Setup & Running

1.  **Clone the repository** (if not already done).

2.  **Environment Setup**:
    - Create a `.env` file in the root (or use the defaults in `docker-compose.yml` for dev).
    - Update `frontend/src/views/HomeView.vue` with your Mapbox Token.

3.  **Run with Docker**:
    ```bash
    docker-compose up -d --build
    ```
    *Note: If you are using Docker Compose V2, use `docker compose up -d --build`.*

4.  **Access the App**:
    - **Frontend**: http://localhost:5173 (or port 80/3000 depending on config, check docker logs)
        - *Note: The current docker-compose maps frontend to port 5173 by default if using `npm run dev -- --host`.*
    - **Backend API**: http://localhost:8000/docs

## Project Structure
- `backend/`: FastAPI application, database models, migrations.
- `frontend/`: Vue 3 application.
- `scraper/`: Event scraping scripts (Playwright).
- `ml_engine/`: Clustering logic (DBSCAN).
- `docker-compose.yml`: Service orchestration.

## Development
- **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```
- **Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## Notes
- The `postgis/postgis` image is used for the database to support geospatial queries.
- Alembic is configured for database migrations.
