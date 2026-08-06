# 📡 IoT & Telemetry Engineering Projects

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Next.js 16](https://img.shields.io/badge/Next.js-16.0-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MQTT](https://img.shields.io/badge/MQTT-HiveMQ%2FThingsBoard-660099?style=for-the-badge&logo=mqtt&logoColor=white)](https://mqtt.org/)
[![Supabase](https://img.shields.io/badge/Supabase-Cloud%2FSQLite-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A curated collection of end-to-end **Internet of Things (IoT)**, **Real-Time Telemetry**, **Cloud Database Storage**, **Orbital Mechanics Analytics**, and **Smart Agriculture Dashboards**. 

This monorepo showcases diverse IoT communication protocols (**MQTT**, **HTTP REST API**, **AJAX Polling**), cloud database routing (**Supabase Cloud**, **SQLite**), real-time visualization frameworks (**Next.js**, **Streamlit**, **Chart.js**, **Matplotlib**), and IoT platform integrations (**ThingsBoard Cloud**).

---

## 📂 Repository Overview

```
IOT-Projects/
├── 🌿 plantiq/       # Smart Agriculture & Plant Care Dashboard (Next.js 16 + React 19 + Tailwind)
├── 🌡️ IoT-Python/    # TempSync Cloud Temperature Monitoring System (Django + Supabase/SQLite)
├── 🛰️ location-iot/  # Real-Time ISS Location & Trajectory Analytics (Python + Open Notify API)
└── ⚡ IoT-CAE1/      # MQTT Telemetry Broker & Streamlit / ThingsBoard Integration
```

---

## 🛠️ Project Matrix & Feature Comparison

| Project | Domain / Scope | Primary Tech Stack | Database / Storage | Protocols & Services | Dashboard / UI |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [**PlantIQ**](./plantiq) | Smart Plant Care & Environmental Monitoring | Next.js 16, React 19, TypeScript, Tailwind CSS | Local / Cloud State | HTTP API, Recharts | Modern React Dashboard |
| [**TempSync**](./IoT-Python) | IoT Temperature Monitoring & Analytics | Django, Python, Chart.js, HTML5/CSS3 | Supabase Cloud / SQLite | HTTP REST, AJAX Polling | Django Admin & Custom Web App |
| [**Location-IoT**](./location-iot) | ISS Space Station Telemetry & Trajectory | Python, Pandas, Matplotlib, Requests | CSV Dataset Logging | Open Notify REST API | Matplotlib Trajectory Maps |
| [**IoT-CAE1**](./IoT-CAE1) | Lightweight MQTT Sensor Telemetry | Python, Paho MQTT, Streamlit, Pandas | Supabase Cloud | MQTT (HiveMQ & ThingsBoard) | Streamlit Metrics & ThingsBoard |

---

## 🔍 Detailed Project Breakdown

### 🌿 1. PlantIQ (`/plantiq`)
> **Smart Environmental & Plant Monitoring Interface**

**PlantIQ** is a modern, high-performance web interface for plant health analytics and automated care recommendations. Built with Next.js 16 App Router, React 19, Lucide Icons, and Recharts.

- **Key Features:**
  - Dynamic plant metrics & environmental condition cards.
  - Interactive moisture, sunlight, and temperature trend visualization using Recharts.
  - Responsive dark-mode dashboard tailored for mobile and desktop screens.
- **Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS v4, Lucide React, Recharts.
- **Quickstart:**
  ```bash
  cd plantiq
  npm install
  npm run dev
  ```

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
- **Tech Stack:** Django, Python, Supabase Python Client, SQLite, Chart.js, HTML5/CSS3.
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
  - **Automated CSV Data Collector:** Captures timestamps, latitude, and longitude into structured datasets.
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

### ⚡ 4. IoT-CAE1 - MQTT Telemetry & Cloud Integration (`/IoT-CAE1`)
> **Lightweight MQTT Publisher/Subscriber Pipeline & Streamlit Control Panel**

**IoT-CAE1** demonstrates core IoT pub/sub networking using MQTT brokers (HiveMQ Public & ThingsBoard Cloud) coupled with a Streamlit telemetry monitoring panel.

- **Key Features:**
  - **MQTT Publisher (`publisher.py`):** Publishes sensor metrics to HiveMQ public broker (`broker.hivemq.com`).
  - **MQTT Subscriber (`subscriber.py`):** Listens to live topics and prints incoming payload streams.
  - **ThingsBoard Cloud Connector (`thingsboard.py`):** Streams JSON telemetry payloads directly to ThingsBoard IoT platform (`eu.thingsboard.cloud`).
  - **Streamlit Telemetry Board (`app.py`):** Real-time web visualization fetching data stored in Supabase tables.
- **Tech Stack:** Python, Paho MQTT, Streamlit, Supabase, Python-dotenv.
- **Quickstart:**
  ```bash
  cd IoT-CAE1
  pip install paho-mqtt streamlit supabase python-dotenv pandas
  streamlit run app.py
  ```

---

## ⚡ Global Setup & Environment Configuration

### Prerequisites
- **Python:** Version 3.8 or higher
- **Node.js:** Version 18.0 or higher (for Next.js / PlantIQ)
- **Git:** Version 2.20 or higher

### Environment Variables Template (`.env.example`)
Create a `.env` file in sub-projects requiring cloud connections (e.g., `IoT-Python` or `IoT-CAE1`):

```env
# Supabase Configuration
SUPABASE_URL=https://your-supabase-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# ThingsBoard Configuration (For IoT-CAE1)
ACCESS_TOKEN=your-thingsboard-device-access-token
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
┌─────────────────┐       Open Notify API        ┌───────────▼────────────┐
│   ISS Telemetry ├────────────────────────────►│ Django / Streamlit UI  │
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
