# BLR Event Discovery Platform

**A hyper-local, AI-driven event recommendation engine designed to connect Bengaluru businesses with the right local opportunities.**

---

## Project Description

In the bustling ecosystem of Bengaluru, small businesses and vendors often struggle to find relevant local events (flea markets, exhibitions, pop-ups) where they can showcase their products. Existing platforms are often cluttered, lack location precision, or don't offer personalized suggestions.

**What This Project Does:**
The BLR Event Discovery Platform aggregates event data from multiple sources (like AllEvents.in), cleans and geocodes it to precise locations, and provides a visual, interactive dashboard. It uses Machine Learning to understand a vendor's business category (e.g., "Fashion", "Food") and recommends the most high-impact events for them.

**Key Features:**
*   **Smart Aggregation**: Automated scrapers (Playwright) fetch real-time event data.
*   **Precision Geocoding**: Converts vague venue names into precise map coordinates using Google Maps/OSM.
*   **AI Recommendations**: A Content-Based Filtering engine matches vendor profiles with event descriptions.
*   **Zone Clustering**: Interactive map clustering for major zones like Indiranagar and Koramangala.

**Challenges Solved:**
*   **Unstructured Data**: Handling inconsistent addresses and missing venue details from raw scraped data.
*   **Scalability**: Using containerization (Docker) to manage complex dependencies like Headless Browsers and MongoDB.
*   **Relevance**: Moving beyond simple keyword search to semantic matching of vendor interests.

---

## Installation and Setup

Follow these steps to get the project running on your local machine.

### Prerequisites
*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Recommended)
*   **OR** Node.js v18+ and Python 3.10+ (for manual setup)

### Method 1: Using Docker (Recommended)
This is the fastest verify to run the full stack (Frontend, Backend, Database) without manual dependency management.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/prakhyathr/Major_project.git
    cd Major_project
    ```

2.  **Build and Start Containers**
    Run the following command in the root directory:
    ```bash
    docker-compose up --build
    ```
    *   This will pull the necessary images and start MongoDB, FastAPI Backend, and Vue3 Frontend.

3.  **Access the Application**
    *   **Frontend Dashboard**: Open [http://localhost:5173](http://localhost:5173) in your browser.
    *   **Backend API Docs**: Open [http://localhost:8000/docs](http://localhost:8000/docs) to see the API endpoints.

### Method 2: Manual Setup

**1. Database Setup**
*   Install and start MongoDB locally on port `27017`.

**2. Backend Setup**
Navigate to the backend folder and install dependencies:
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
python main.py
```

**3. Frontend Setup**
Navigate to the frontend folder and install dependencies:
```bash
cd frontend
npm install
npm run dev
```

---

## Usage Instructions

Once the application is running, follow these steps to explore the platform:

**1. Registration / Login**
*   On the landing page, click **"Register as a Vendor"**.
*   Enter your business details and select your **Interests** (e.g., Music, Food, Art). This is crucial for the AI recommendations.
*   Login with your credentials.

**2. Exploring the Map**
*   The **Dashboard** is split into a Map View (left) and an Event List (right).
*   **Clusters**: Click on the colored circles (Clusters) on the map to zoom into specific areas like *Indiranagar* or *Whitefield*.
*   **Zone Chips**: Use the quick-filter chips at the top of the map to jump to popular zones.

**3. Finding Events**
*   **Filter by Category**: Use the dropdown to select specific types of events (e.g., "Parties", "Workshops").
*   **Search**: Type keywords to find specific events.
*   **Logout**: Click the "Logout" button in the top right corner to exit.

**4. AI Recommendations**
*   The **"Recommended for You"** section highlights the top 5 events that match your business profile.
*   Click **"View"** on any event card to visit the official event page and book tickets.

---

## Tech Stack Overview

### Frontend (User Interface)
*   **Vue.js 3**: The core framework, utilizing the **Composition API** and **`<script setup>`** for clean, reactive logic.
*   **Vite**: Next-generation build tool that provides lightning-fast Hot Module Replacement (HMR) during development.
*   **Tailwind CSS**: A utility-first CSS framework for rapidly building custom designs without writing custom CSS.
*   **Leaflet.js**: An open-source JavaScript library for interactive maps.
*   **Leaflet.markercluster**: A plugin to manage map clutter by grouping nearby event markers into clusters.

### Backend (API & Logic)
*   **FastAPI**: A modern, high-performance web framework for building APIs with Python 3.10+, based on standard Python type hints.
*   **Uvicorn**: An ASGI web server implementation for Python.
*   **Pydantic**: Data validation and settings management using Python type annotations.
*   **Motor**: Asynchronous Python driver for MongoDB, allowing non-blocking database operations.

### Database
*   **MongoDB (v6.0)**: A NoSQL database chosen for its flexibility in storing unstructured event data and its powerful geospatial query capabilities (`$near`, `$geometry`).

### Machine Learning & Data Pipeline
*   **Sentence-Transformers (BERT)**: Upgraded from TF-IDF to the **`all-MiniLM-L6-v2`** model. This enables **Semantic Matching** (understanding that "Coding" = "Programming"), improving recommendation relevance by **2.5x** (Coverage Score: ~49%).
*   **Pandas & NumPy**: For efficient data manipulation and analysis during the ML training process.
*   **Playwright**: A Python library to automate Chromium browsers, used to scrape dynamic content from event websites (e.g., BookMyShow, AllEvents).
*   **BeautifulSoup4**: HTML parser for extracting data from static page content.

### DevOps & Infrastructure
*   **Docker**: Containerization platform to ensure the application runs consistently across different environments.
*   **Docker Compose**: Tool for defining and running multi-container Docker applications (Frontend, Backend, Database).
