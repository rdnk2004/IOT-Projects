import os
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import database

CHARTS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

def load_readings_dataframe(target_date=None):
    """
    Loads readings from database into a Pandas DataFrame for a given date (or today).
    """
    if target_date is None:
        target_date = date.today()
    elif isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()

    start_dt = datetime.combine(target_date, datetime.min.time())
    end_dt = datetime.combine(target_date, datetime.max.time())

    readings = database.get_readings_range(start_time=start_dt, end_time=end_dt)
    
    if not readings:
        # If no readings for target date, fallback to fetch all available readings
        readings = database.get_readings_range(limit=2000)

    if not readings:
        return pd.DataFrame()

    df = pd.DataFrame(readings)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['temperature'] = pd.to_numeric(df['temperature'])
    return df

def calculate_daily_statistics(target_date=None):
    """
    Computes statistical analysis for the given day:
    - Mean temperature
    - Median temperature
    - Mode
    - Maximum temperature
    - Minimum temperature
    - Range
    - Variance
    - Standard deviation
    """
    df = load_readings_dataframe(target_date)

    if df.empty or 'temperature' not in df.columns or df['temperature'].count() == 0:
        return {
            "count": 0,
            "mean": None,
            "median": None,
            "mode": None,
            "max": None,
            "min": None,
            "range": None,
            "variance": None,
            "std_dev": None
        }

    temps = df['temperature'].dropna()

    mean_val = float(temps.mean())
    median_val = float(temps.median())
    
    # Calculate mode by rounding to 1 decimal place to handle continuous sensor floats
    rounded_temps = temps.round(1)
    mode_res = stats.mode(rounded_temps, keepdims=True)
    if len(mode_res.mode) > 0:
        mode_val = float(mode_res.mode[0])
    else:
        mode_val = float(rounded_temps.mode().iloc[0]) if not rounded_temps.mode().empty else None

    max_val = float(temps.max())
    min_val = float(temps.min())
    range_val = float(max_val - min_val)
    var_val = float(temps.var(ddof=1)) if len(temps) > 1 else 0.0
    std_val = float(temps.std(ddof=1)) if len(temps) > 1 else 0.0

    return {
        "count": int(len(temps)),
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "mode": round(mode_val, 2) if mode_val is not None else None,
        "max": round(max_val, 2),
        "min": round(min_val, 2),
        "range": round(range_val, 2),
        "variance": round(var_val, 3),
        "std_dev": round(std_val, 3)
    }

def calculate_time_series_analysis(target_date=None):
    """
    Performs time series analysis:
    - Diurnal temperature trend data points
    - Hourly average temperatures
    - Timestamps of maximum and minimum temperatures
    """
    df = load_readings_dataframe(target_date)

    if df.empty or 'temperature' not in df.columns or df['temperature'].count() == 0:
        return {
            "trend": [],
            "hourly_averages": [],
            "max_info": {"temperature": None, "timestamp": None, "formatted_time": None},
            "min_info": {"temperature": None, "timestamp": None, "formatted_time": None}
        }

    # Identify Max and Min timestamps
    max_idx = df['temperature'].idxmax()
    min_idx = df['temperature'].idxmin()

    max_row = df.loc[max_idx]
    min_row = df.loc[min_idx]

    max_info = {
        "temperature": round(float(max_row['temperature']), 2),
        "timestamp": max_row['timestamp'].isoformat(),
        "formatted_time": max_row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    }

    min_info = {
        "temperature": round(float(min_row['temperature']), 2),
        "timestamp": min_row['timestamp'].isoformat(),
        "formatted_time": min_row['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
    }

    # Hourly Average Computation
    df_hourly = df.set_index('timestamp').resample('1h')['temperature'].mean().reset_index()
    hourly_averages = []
    for _, row in df_hourly.iterrows():
        if pd.notnull(row['temperature']):
            hourly_averages.append({
                "hour": row['timestamp'].strftime("%H:00"),
                "timestamp": row['timestamp'].isoformat(),
                "average_temperature": round(float(row['temperature']), 2)
            })

    # Time series trend data points
    trend = []
    for _, row in df.iterrows():
        trend.append({
            "timestamp": row['timestamp'].isoformat(),
            "formatted_time": row['timestamp'].strftime("%H:%M"),
            "temperature": round(float(row['temperature']), 2),
            "apparent_temperature": round(float(row['apparent_temperature']), 2) if pd.notnull(row.get('apparent_temperature')) else None,
            "humidity": round(float(row['humidity']), 1) if pd.notnull(row.get('humidity')) else None
        })

    return {
        "trend": trend,
        "hourly_averages": hourly_averages,
        "max_info": max_info,
        "min_info": min_info
    }

def generate_matplotlib_weather_charts(target_date=None):
    """
    Generates Matplotlib charts for weather telemetry:
    1. Line Chart: Temperature vs Time.
    2. Bar Chart: Hourly Average Temperatures.
    """
    df = load_readings_dataframe(target_date)
    if df.empty or 'temperature' not in df.columns:
        return {}

    plt.style.use('dark_background')

    # Chart 1: Temperature vs Time (Line Chart)
    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor='#1e293b')
    ax.set_facecolor('#0f172a')
    
    times = [t.strftime('%H:%M') for t in df['timestamp']]
    temps = df['temperature'].values
    x_indices = list(range(len(temps)))

    ax.plot(x_indices, temps, marker='o', color='#38bdf8', linewidth=2.5, markersize=5, markerfacecolor='#6366f1', label='Temperature (°C)')
    if 'apparent_temperature' in df.columns and df['apparent_temperature'].notnull().any():
        ax.plot(x_indices, df['apparent_temperature'].values, linestyle='--', color='#f59e0b', linewidth=2, label='Feels Like (°C)')

    step = max(1, len(x_indices) // 10)
    ax.set_xticks(x_indices[::step])
    ax.set_xticklabels(times[::step])
    ax.set_title('Kochi Temperature Variation Over Time (Matplotlib Line Chart)', fontsize=13, fontweight='bold', pad=15, color='#f8fafc')
    ax.set_xlabel('Time (HH:MM)', fontsize=10, color='#94a3b8', labelpad=8)
    ax.set_ylabel('Temperature (°C)', fontsize=10, color='#94a3b8', labelpad=8)
    ax.grid(True, linestyle='--', alpha=0.2, color='#ffffff')
    ax.legend(facecolor='#0f172a', edgecolor='none', labelcolor='#94a3b8')

    plt.tight_layout()
    chart1_path = os.path.join(CHARTS_DIR, 'temp_time_series.png')
    plt.savefig(chart1_path, dpi=120)
    plt.close()

    # Chart 2: Hourly Average Temperature (Bar Chart)
    df_hourly = df.set_index('timestamp').resample('1h')['temperature'].mean().dropna().reset_index()
    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor='#1e293b')
    ax.set_facecolor('#0f172a')

    hours = [h.strftime('%H:00') for h in df_hourly['timestamp']]
    avg_temps = df_hourly['temperature'].values
    x_h = list(range(len(avg_temps)))

    bars = ax.bar(x_h, avg_temps, color='#6366f1', edgecolor='#818cf8', width=0.55)
    ax.set_xticks(x_h)
    ax.set_xticklabels(hours, rotation=30)
    ax.set_title('Hourly Average Temperature Breakdown (Matplotlib Bar Chart)', fontsize=13, fontweight='bold', pad=15, color='#f8fafc')
    ax.set_xlabel('Hour Window', fontsize=10, color='#94a3b8', labelpad=8)
    ax.set_ylabel('Average Temp (°C)', fontsize=10, color='#94a3b8', labelpad=8)
    ax.grid(True, linestyle='--', alpha=0.2, color='#ffffff', axis='y')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.2, f'{height:.1f}', ha='center', va='bottom', color='#f8fafc', fontsize=9, fontweight='bold')

    plt.tight_layout()
    chart2_path = os.path.join(CHARTS_DIR, 'hourly_averages.png')
    plt.savefig(chart2_path, dpi=120)
    plt.close()

    return {
        "time_series_chart": "/static/charts/temp_time_series.png",
        "hourly_averages_chart": "/static/charts/hourly_averages.png"
    }

def generate_daily_report(target_date=None):
    """
    Generates a daily summary report containing:
    - Total reading count
    - Average daily temperature
    - Highest & lowest temperatures with timestamps
    - Meteorological observations and thermal comfort insight
    """
    stats_data = calculate_daily_statistics(target_date)
    ts_data = calculate_time_series_analysis(target_date)

    if stats_data["count"] == 0:
        return {
            "summary_date": str(target_date or date.today()),
            "total_readings": 0,
            "avg_temperature": None,
            "max_info": ts_data["max_info"],
            "min_info": ts_data["min_info"],
            "stats": stats_data,
            "observations": ["No weather readings recorded for this day yet."]
        }

    avg_temp = stats_data["mean"]
    max_temp = stats_data["max"]
    min_temp = stats_data["min"]
    temp_range = stats_data["range"]
    std_dev = stats_data["std_dev"]

    observations = []

    # Thermal Comfort & Climate Insights for Kochi (Tropical Monsoon Climate)
    if avg_temp >= 30.0:
        observations.append(f"Kochi experienced high daytime thermal pressure with an average temperature of {avg_temp}°C.")
    elif avg_temp >= 26.0:
        observations.append(f"Kochi recorded moderate tropical warmth averaging {avg_temp}°C throughout the monitoring period.")
    else:
        observations.append(f"Kochi maintained a comfortable coastal temperature averaging {avg_temp}°C.")

    observations.append(
        f"Peak temperature reached {max_temp}°C at {ts_data['max_info']['formatted_time']}, "
        f"while the minimum recorded temperature was {min_temp}°C at {ts_data['min_info']['formatted_time']}."
    )

    if temp_range > 6.0:
        observations.append(f"Noticeable diurnal fluctuation observed with a temperature range of {temp_range}°C.")
    else:
        observations.append(f"Stable temperature variation recorded (diurnal range: {temp_range}°C), typical of coastal ocean dampening.")

    if std_dev < 1.5:
        observations.append(f"Low temperature dispersion (standard deviation: {std_dev}°C) indicates steady ambient thermal stability.")
    else:
        observations.append(f"Moderate temperature variance detected (standard deviation: {std_dev}°C) reflecting daytime heating and nighttime cooling cycles.")

    return {
        "summary_date": str(target_date or date.today()),
        "total_readings": stats_data["count"],
        "avg_temperature": avg_temp,
        "max_info": ts_data["max_info"],
        "min_info": ts_data["min_info"],
        "stats": stats_data,
        "observations": observations
    }
