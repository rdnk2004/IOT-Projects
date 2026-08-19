# 📡 IoT & Telemetry Engineering Projects

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16.0-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Flask 3.0+](https://img.shields.io/badge/Flask-3.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Django 4.2+](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MQTT](https://img.shields.io/badge/MQTT-HiveMQ%2FThingsBoard-660099?style=for-the-badge&logo=mqtt&logoColor=white)](https://mqtt.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Cloud%2FSQLite-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A curated collection of end-to-end **Internet of Things (IoT)**, **Real-Time Telemetry Systems**, **Cloud & Relational Database Storage**, **Seismic & Climate Data Analytics**, **Orbital Mechanics Analytics**, and **Smart Agriculture Dashboards**.

This monorepo showcases diverse IoT communication protocols (**MQTT**, **HTTP REST API**, **AJAX Polling**), cloud and local database routing (**Supabase Cloud**, **SQLite**, **SQLAlchemy ORM**), real-time visualization frameworks (**Next.js**, **Flask**, **Streamlit**, **Chart.js**, **Matplotlib**, **Recharts**), background scheduling (**APScheduler**), and IoT platform integrations (**ThingsBoard Cloud**).

---

## 📂 Repository Overview

```
IOT-Projects/
├── 🌿 plantiq/               # Smart Agriculture & Plant Care Dashboard (Next.js 16 + React 19 + Tailwind)
├── 🌡️ IoT-Python/            # TempSync Cloud Temperature Monitoring System (Django + Supabase/SQLite)
├── 🛰️ location-iot/          # Real-Time ISS Location & Trajectory Analytics (Python + Open Notify API)
├── ⚡ IoT-CAE1/              # MQTT Telemetry Broker & Streamlit / ThingsBoard Integration
├── 🌤️ weather_monitoring/    # Real-Time Weather Telemetry & Climate Analytics System (Flask + Open-Meteo API)
└── 🌋 earthquake_analytics/ # USGS Real-Time Seismic Telemetry & Earthquake Analytics (Flask + USGS API)
```

---

## 🛠️ Project Matrix & Feature Comparison

| Project | Domain / Scope | Primary Tech Stack | Database / Storage | Protocols & Services | Dashboard / UI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [**PlantIQ**](./plantiq) | Smart Plant Care & Environmental Monitoring | Next.js 16, React 19, TypeScript, Tailwind CSS | Local / Cloud State | HTTP API, Recharts | Modern React Dashboard |
| [**TempSync**](./IoT-Python) | IoT Temperature Monitoring & Analytics | Django, Python, Chart.js, HTML5/CSS3 | Supabase Cloud / SQLite | HTTP REST, AJAX Polling | Django Admin & Custom Web App |
| [**Location-IoT**](./location-iot) | ISS Space Station Telemetry & Trajectory | Python, Pandas, Matplotlib, Requests | CSV Dataset Logging | Open Notify REST API | Matplotlib Trajectory Maps |
| [**IoT-CAE1**](./IoT-CAE1) | Lightweight MQTT Sensor Telemetry | Python, Paho MQTT, Streamlit, Pandas | Supabase Cloud | MQTT (HiveMQ & ThingsBoard) | Streamlit Metrics & ThingsBoard |
| [**Weather Monitoring**](./weather_monitoring) | Kochi Weather Telemetry & Climate Analytics | Flask, SQLAlchemy, APScheduler, SciPy, Matplotlib | SQLite (`kochi_weather.db`) | Open-Meteo REST API | Flask Web UI & Matplotlib Charts |
| [**Earthquake Analytics**](./earthquake_analytics) | USGS Real-Time Seismic Event Analytics | Flask, Pandas, NumPy, Matplotlib, Requests | GeoJSON Cache | USGS GeoJSON REST API | Flask Web UI & REST API |

---

## 🔍 Detailed Project Breakdown

### 🌿 1. PlantIQ (`/plantiq`)
> **Smart Environmental & Plant Monitoring Interface**

**PlantIQ** is a modern, high-performance web interface for plant health analytics and automated care recommendations. Built with Next.js 16 App Router, React 19, Lucide Icons, and Recharts.

- **Key Features:**
  - Dynamic plant metrics & environmental condition cards (soil moisture, temperature, sunlight, humidity).
  - Interactive moisture, sunlight, and temperature trend visualization using Recharts.
  - Smart care recommendation engine tailored for plant care actions.
  - Responsive dark-mode dashboard tailored for mobile and desktop screens.
- **Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS v4, Lucide React, Recharts.
- **Quickstart:**
  ```bash
  cd plantiq
  npm install
  npm run dev
  ```
  *(Runs on `http://localhost:3000`)*

---

### 🌡️ 2. TempSync - IoT Temperature Monitoring (`/IoT-Python`)
> **Cloud-Connected Real-Time Sensor Telemetry Engine**

**TempSync** is an enterprise-ready temperature monitoring system powered by Django. It includes an automated synthetic sensor generator pushing simulated hardware readings, dual-database failover routing, and real-time Chart.js visualizations.

- **Key Features:**
  - **Synthetic Sensor Simulator:** Virtual IoT node generating periodic telemetry ($20^\circ\text{C} - 40^\circ\text{C}$).
  - **Dual Database Architecture:** Dynamic routing to **Supabase Cloud** when online, with automatic seamless fallback to local **SQLite** (`data.sqlite3`).
  - **Analytics Engine:** Instant minimum, maximum, average temperature calculation and range filtering.
  - **Live AJAX Polling:** 5-second asynchronous UI refresh without full page reloads.
  - **Data Export:** Instant CSV reporting for telemetry audit logs.
- **Tech Stack:** Django 4.2+, Python 3.8+, Supabase Python Client, SQLite, Chart.js, HTML5/CSS3.
- **Quickstart:**
  ```bash
  cd IoT-Python
  pip install -r requirements.txt
  python manage.py migrate
  python sensor_simulator.py  # In Terminal 1 (Sensor)
  python manage.py runserver  # In Terminal 2 (Server)
  ```

---

### 🛰️ 3. Location-IoT - ISS Trajectory Tracking (`/location-iot`)
> **Orbital Telemetry Stream & Spatial Trajectory Visualization**

**Location-IoT** streams real-time geographic coordinates of the International Space Station (ISS) orbiting Earth at approximately $28,000 \text{ km/h}$. The system logs spatial datasets and generates orbital trajectory plots.

- **Key Features:**
  - **Telemetry Streaming:** Polls Open Notify API (`/iss-now.json`) at customizable intervals.
  - **Automated CSV Data Collector:** Captures timestamps, latitude, and longitude into structured datasets (`iss_location_data.csv`).
  - **Orbital Mechanics Analytics:** Calculates spatial extremes, average latitude/longitude position, velocity trends, and directional vectors.
  - **Visualization Suite:** Produces high-resolution Matplotlib graphs:
    - Latitude vs. Time (`latitude_vs_time.png`)
    - Longitude vs. Time (`longitude_vs_time.png`)
    - 2D Orbital Flight Path Map (`iss_trajectory_map.png`)
- **Tech Stack:** Python 3.8+, Pandas, Matplotlib, Requests.
- **Quickstart:**
  ```bash
  cd location-iot
  python main.py
  ```

---

### ⚡ 4. IoT-CAE1 - Multi-Protocol IoT & Telemetry Lab (`/IoT-CAE1`)
> **Modular Suite: Supabase Cloud Telemetry, MQTT Pub/Sub Pipeline & ThingsBoard Integration**

**IoT-CAE1** provides three modular IoT programs showcasing pub/sub networking, relational cloud database persistence, and commercial IoT cloud platform integration:

- **1. Supabase Temperature Monitor (`/supabase-temp-monitor`):** Real-time Streamlit dashboard (`app.py`) fetching telemetry stored in Supabase Cloud, populated by automated sensor script (`send_temp.py`).
- **2. MQTT Pub/Sub Pipeline (`/mqtt-pub-sub`):** Lightweight publisher (`publisher.py`) and subscriber (`subscriber.py`) over standard MQTT via HiveMQ public broker.
- **3. ThingsBoard Cloud Telemetry (`/thingsboard-telemetry`):** Authenticated device client (`thingsboard.py`) publishing JSON telemetry directly to ThingsBoard Cloud.

- **Tech Stack:** Python, Paho MQTT, Streamlit, Supabase, Python-dotenv, Pandas.
- **Quickstart:**
  ```bash
  cd IoT-CAE1/supabase-temp-monitor && streamlit run app.py
  # Or explore mqtt-pub-sub / thingsboard-telemetry
  ```

---

### 🌤️ 5. Weather Monitoring (`/weather_monitoring`)
> **Real-Time Weather Telemetry & Climate Analytics System**

**Weather Monitoring** is an automated Flask telemetry service fetching live ambient weather metrics for Kochi from the Open-Meteo API. It stores telemetry data into an SQLite relational database via SQLAlchemy, computes statistical distributions (including mode via SciPy), and auto-generates headless Matplotlib climate charts.

- **Key Features:**
  - **Automated Background Scheduler:** APScheduler background worker fetching live sensor metrics every 5 minutes.
  - **Database Persistence & Seeding:** Persistent SQLite storage with 24-hour historical seed backfilling.
  - **Statistical Analysis Engine:** Computes mean, median, mode (via SciPy), min/max, range, variance, and standard deviation.
  - **Matplotlib Visualization Pipeline:** Automatically generates headless time-series plots and hourly temperature breakdown charts (`static/charts/`).
  - **REST API Suite:** Endpoints for current weather (`/api/current`), historical readings (`/api/history`), daily stats (`/api/stats`), time series (`/api/timeseries`), and daily reports (`/api/report`).
- **Tech Stack:** Flask 3.0+, SQLAlchemy, APScheduler, Open-Meteo API, Pandas, NumPy, SciPy, Matplotlib.
- **Quickstart:**
  ```bash
  cd weather_monitoring
  pip install -r requirements.txt
  python app.py
  ```
  *(Launches on `http://127.0.0.1:5000`)*

---

### 🌋 6. Earthquake Analytics (`/earthquake_analytics`)
> **USGS Real-Time Seismic Telemetry & Earthquake Analytics Dashboard**

**Earthquake Analytics** is a Flask-powered telemetry monitoring platform that ingests global seismic event data from the United States Geological Survey (USGS) GeoJSON API over a 7-day rolling window. It processes magnitude distributions, identifies peak seismic activity days, and visualizes high-impact events.

- **Key Features:**
  - **Live USGS Feed Integration:** Real-time GeoJSON ingestion capturing magnitude, location, depth, timestamp, tsunami warnings, and significance score.
  - **Statistical Metrics:** Calculates seismic magnitude mean, median, standard deviation, variance, and min/max extremes.
  - **Time-Series Analysis:** Daily event counts and automatic detection of peak seismic activity days.
  - **Seismic Leaderboard:** Ranks top-N strongest earthquakes globally with direct links to USGS event reports.
  - **Dynamic Matplotlib Charts:** Headless generation of seismic frequency histograms and time-series distribution plots (`static/charts/`).
  - **REST API Endpoints:** JSON API endpoints for stats (`/api/stats`), time series (`/api/timeseries`), top events (`/api/top`), and force refresh (`/api/refresh`).
- **Tech Stack:** Flask 3.0+, Requests, Pandas, NumPy, Matplotlib, USGS GeoJSON API.
- **Quickstart:**
  ```bash
  cd earthquake_analytics
  pip install -r requirements.txt
  python app.py
  ```
  *(Launches on `http://127.0.0.1:5001`)*

---

## ⚡ Global Setup & Environment Configuration

### Prerequisites
- **Python:** Version 3.8 or higher
- **Node.js:** Version 18.0 or higher (for Next.js / PlantIQ)
- **Git:** Version 2.20 or higher

### Environment Variables Template (`.env.example`)
Create a `.env` file in sub-projects requiring cloud connections (e.g., `IoT-Python`, `IoT-CAE1`, or `weather_monitoring`):

```env
# Supabase Configuration (For IoT-Python & IoT-CAE1)
SUPABASE_URL=https://your-supabase-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# ThingsBoard Configuration (For IoT-CAE1)
ACCESS_TOKEN=your-thingsboard-device-access-token

# Weather Monitoring Flask Configuration
FLASK_SECRET_KEY=your-custom-secret-key
```

---

## 📡 Architecture & Telemetry Protocols

```
┌─────────────────┐       MQTT (Port 1883)       ┌────────────────────────┐
│  IoT Publisher  ├────────────────────────────►│  HiveMQ / ThingsBoard  │
└─────────────────┘                              └───────────┬────────────┘
                                                             │
┌─────────────────┐       HTTP REST API          ┌───────────▼────────────┐
│   Sensor Node   ├────────────────────────────►│   Supabase Cloud DB    │
└─────────────────┘                              └───────────┬────────────┘
                                                             │
┌─────────────────┐   Open-Meteo & USGS APIs     ┌───────────▼────────────┐
│ Weather & USGS  ├────────────────────────────►│ Flask / Streamlit /    │
│ Telemetry Feeds │                              │ Django UI Dashboards   │
└─────────────────┘                              └────────────────────────┘
```

---

## 🤝 Contributing & Guidelines

Contributions are welcome! Please follow these steps when proposing updates:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/AmazingIoTFeature`.
3. Commit your changes: `git commit -m 'Add some AmazingIoTFeature'`.
4. Push to the branch: `git push origin feature/AmazingIoTFeature`.
5. Open a Pull Request.

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Developed with ❤️ for Advanced IoT, Space Telemetry & Embedded Systems Engineering.
</p>

