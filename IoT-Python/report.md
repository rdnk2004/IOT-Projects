# Project Report: Cloud-Based Temperature Monitoring System

## 1. Introduction
The objective of this project is to design, implement, and verify a cloud-based temperature monitoring system. The system consists of two primary parts:
1. **An IoT Sensor Simulator (Python)**: Generates random temperature readings representing an actual sensor, formats timestamps, and uploads them to a cloud database or a local backup database.
2. **A Web Application Dashboard (Django)**: Retrieves historical data, computes real-time statistics (Latest, Average, Minimum, Maximum), maps values on a visual trend line chart (Chart.js), lists logs in a paginated table, and exports data to CSV format.

To ensure robustness, the system features a dual-database routing model that securely integrates with **Supabase Cloud (PostgreSQL)** when credentials are provided, and automatically falls back to an offline local **SQLite database** when credentials are absent or connection issues arise.

---

## 2. System Architecture & Workflow

The architecture is built on a clean decoupling of the data producer (sensor) and the data consumer (web dashboard) interacting through a unified database layer.

```
       +---------------------------------------------+
       |         IoT Sensor Simulator (Python)       |
       |      - Generates temperature every 5s       |
       +----------------------++---------------------+
                              || Writes Data
                              \/
       +---------------------------------------------+
       |          Database Router (database.py)       |
       |  Routes queries dynamically based on .env   |
       +-------++----------------------------++------+
               || If credentials              || Fallback / Offline
               \/                             \/
       +---------------------+        +--------------+
       |   Supabase Cloud    |        | Local SQLite |
       |    (PostgreSQL)     |        | (data.sqlite)|
       +-------++------------+        +------++------+
               ||                            ||
               +--------------++-------------+
                              || Reads Data
                              \/
       +---------------------------------------------+
       |         Django Web App Controller           |
       |     - Manages routes & user sessions        |
       |     - API views (JSON readings, CSV export) |
       +----------------------++---------------------+
                              || Serves Assets
                              \/
       +---------------------------------------------+
       |         HTML5/CSS3/JS Web Interface         |
       |    - Session login & secure dashboard       |
       |    - AJAX polling every 5s for auto-refresh |
       |    - Chart.js Line Chart & Data Table       |
       +---------------------------------------------+
```

### System Workflow
1. The **IoT Sensor** script starts in a loop, generating a random temperature between 20°C and 40°C every 5 seconds.
2. The sensor formats the reading with the current date, time, and timestamp.
3. The **Database Router** attempts to upload the record to Supabase. If credentials are missing or the upload fails, it backs up the reading in the local SQLite database (`data.sqlite3`).
4. The **Django Server** boots and serves the web dashboard. Unauthenticated users are intercepted by a login view and redirected to a login page.
5. Once a user logs in (credentials: `admin` / `admin123`), the dashboard HTML and assets are rendered.
6. The frontend JavaScript makes an initial AJAX call to the Django REST endpoint `/api/readings/` to retrieve records.
7. JavaScript initializes **Chart.js** to map the chronological trend line and loads the historical data table.
8. If **Auto Refresh** is toggled on, the browser polls the API endpoint every 5 seconds, checking for new data points and updating the chart, metrics cards, and table dynamically without page reloads.
9. Users can filter data by selecting date boundaries. Filtered data updates all dashboard visualizers instantly and can be downloaded as a CSV file.

---

## 3. Database Design & Schemas

The database schemas are standardized across both SQL engines (PostgreSQL on Supabase and SQLite local database) to ensure uniform data ingestion and query behavior.

### Table Schema: `temperature_readings`

| Column Name | Data Type (Supabase) | Data Type (SQLite) | Description | Example Value |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `bigint` (Identity) | `INTEGER` (Primary Key Auto) | Unique incrementing identifier for each log | `42` |
| `temperature` | `float8` (Double precision) | `REAL` | Measured temperature in Celsius (°C) | `26.8` |
| `date` | `text` | `TEXT` | Log date in YYYY-MM-DD format | `2026-07-10` |
| `time` | `text` | `TEXT` | Log time in HH:MM:SS format | `11:24:28` |
| `timestamp` | `float8` (Epoch seconds) | `REAL` | Unix epoch time for chronological sorting | `1783663468.0` |

---

## 4. Key Implementation Details

### Database Routing (`database.py`)
The router loads `.env` variables. If `SUPABASE_URL` and `SUPABASE_KEY` are defined and valid, it initializes the Python `supabase` client. Database writes (`insert_reading`) and reads (`get_readings`) are wrapped in try-catch handlers. If the Supabase request fails, the method prints a console log and routes the instruction to local SQLite, ensuring zero data loss and uninterrupted server operation.

### Session Authentication & User Bootstrapping
Django's built-in session framework was used to protect dashboard routes. Rather than requiring users to manually run commands to create an admin login, Django's `post_migrate` signal was connected to an app-level bootstrapping function in `apps.py`. When migrations finish, the database is queried, and a default superuser (`admin` / `admin123`) is generated automatically.

### AJAX Data Synchronization & Charting
A dedicated REST view (`/api/readings/`) serves JSON arrays of database records and pre-calculated statistics. On the front end, Chart.js parses timestamps and plots them on the horizontal x-axis, using custom blue color fills and grid layouts. Client-side pagination divides logs into blocks of 10 rows per page to prevent page slowdowns as data sizes scale.

---

## 5. Operations & Execution Guide

### Prerequisites
- Python 3.8 or higher installed on the system.

### Installation
1. Extract or place the workspace files in a directory.
2. Open a terminal in the project directory and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the System (Local Fallback Mode)
1. **Initialize the Web Server database**:
   Run migrations to set up the authentication backend:
   ```bash
   python manage.py migrate
   ```
   *(Note: This command will automatically output a message confirming the creation of the default superuser `admin / admin123`).*

2. **Start the Web Dashboard**:
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```
   The dashboard is now accessible at `http://127.0.0.1:8000/`.

3. **Start the Sensor Simulator**:
   Open a separate terminal window and launch the simulator script:
   ```bash
   python sensor_simulator.py
   ```
   You will see temperature logs and successful SQLite write messages printing to the console every 5 seconds.

4. **Access the Dashboard**:
   Open `http://127.0.0.1:8000/`, log in using `admin` / `admin123`, and watch the graph update in real-time.

### Running with Supabase Cloud
1. Create a free account on [Supabase](https://supabase.com/).
2. Create a new project.
3. Open the **SQL Editor** in your Supabase dashboard and run:
   ```sql
   CREATE TABLE temperature_readings (
       id bigint GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
       temperature float8 NOT NULL,
       date text NOT NULL,
       time text NOT NULL,
       timestamp float8 NOT NULL
   );
   ```
4. Go to **Project Settings > API** in Supabase and copy the **Project URL** and **anon public API key**.
5. Open the `.env` file in the root of the project and paste the values:
   ```ini
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
6. Restart both the simulator and web server. The dashboard connection status in the header will update to **Supabase Cloud**, and data will instantly flow to the cloud.
