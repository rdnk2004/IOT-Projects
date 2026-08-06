import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Non-interactive headless renderer for web applications
import matplotlib.pyplot as plt
import fetcher

# Base directory for saving generated Matplotlib charts
CHARTS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

def process_earthquake_dataframe(records=None):
    """
    Converts raw GeoJSON records into a structured Pandas DataFrame
    with parsed datetime timestamps and sorted dates.
    """
    if records is None:
        records = fetcher.fetch_usgs_earthquake_data()
        
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    # Convert Unix timestamp ms to Datetime UTC
    df['datetime'] = pd.to_datetime(df['time_ms'], unit='ms')
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    df['formatted_time'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Sort chronologically
    df = df.sort_values('datetime', ascending=True).reset_index(drop=True)
    return df

def calculate_statistics(df):
    """
    Calculates statistical metrics across earthquake magnitudes:
    - Total number of earthquakes
    - Mean magnitude
    - Median magnitude
    - Standard deviation
    - Variance
    - Minimum and maximum magnitude
    """
    if df.empty or 'magnitude' not in df.columns:
        return {
            "total_count": 0,
            "mean_magnitude": 0.0,
            "median_magnitude": 0.0,
            "std_dev": 0.0,
            "variance": 0.0,
            "min_magnitude": 0.0,
            "max_magnitude": 0.0
        }

    mags = df['magnitude'].dropna()

    return {
        "total_count": int(len(mags)),
        "mean_magnitude": round(float(mags.mean()), 2),
        "median_magnitude": round(float(mags.median()), 2),
        "std_dev": round(float(mags.std(ddof=1)), 3) if len(mags) > 1 else 0.0,
        "variance": round(float(mags.var(ddof=1)), 3) if len(mags) > 1 else 0.0,
        "min_magnitude": round(float(mags.min()), 2),
        "max_magnitude": round(float(mags.max()), 2)
    }

def calculate_time_series(df):
    """
    Performs time series analysis:
    - Counts daily earthquake occurrences
    - Identifies the day with the highest seismic activity
    """
    if df.empty or 'date' not in df.columns:
        return {
            "daily_counts": [],
            "peak_day": None,
            "peak_count": 0
        }

    # Group by date and count occurrences
    daily_series = df.groupby('date').size()
    daily_counts = [{"date": str(d), "count": int(c)} for d, c in daily_series.items()]

    # Identify date with maximum count
    if not daily_series.empty:
        peak_date = str(daily_series.idxmax())
        peak_count = int(daily_series.max())
    else:
        peak_date = None
        peak_count = 0

    return {
        "daily_counts": daily_counts,
        "peak_day": peak_date,
        "peak_count": peak_count
    }

def generate_visualizations(df):
    """
    Generates required Matplotlib charts:
    1. Line chart showing daily earthquake occurrences.
    2. Bar chart of top 10 strongest earthquakes.
    Saves PNG charts into static/charts/.
    """
    if df.empty:
        return {}

    plt.style.use('dark_background')
    
    # 1. Line Chart: Daily Earthquake Occurrences
    daily_series = df.groupby('date').size()
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='#1e293b')
    ax.set_facecolor('#0f172a')
    
    dates = [d[-5:] for d in daily_series.index] # MM-DD formatting for clean x-axis
    counts = daily_series.values
    x_indices = list(range(len(counts)))
    
    ax.plot(x_indices, counts, marker='o', color='#38bdf8', linewidth=2.5, markersize=8, markerfacecolor='#6366f1', label='Daily Earthquakes')
    ax.fill_between(x_indices, counts, color='#38bdf8', alpha=0.15)
    ax.set_xticks(x_indices)
    ax.set_xticklabels(dates)
    
    ax.set_title('Daily Earthquake Occurrences (Past 7 Days)', fontsize=14, fontweight='bold', pad=15, color='#f8fafc')
    ax.set_xlabel('Date (MM-DD)', fontsize=11, color='#94a3b8', labelpad=10)
    ax.set_ylabel('Number of Earthquakes', fontsize=11, color='#94a3b8', labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.2, color='#ffffff')
    ax.tick_params(colors='#94a3b8')
    
    # Value annotations on data points
    for i, txt in enumerate(counts):
        ax.annotate(str(txt), (x_indices[i], counts[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#f8fafc', fontweight='bold')


    plt.tight_layout()
    line_chart_path = os.path.join(CHARTS_DIR, 'daily_occurrences.png')
    plt.savefig(line_chart_path, dpi=120)
    plt.close()

    # 2. Bar Chart: Top 10 Strongest Earthquakes
    top10_df = df.sort_values('magnitude', ascending=False).head(10).iloc[::-1] # Reverse for horizontal bar plot
    
    fig, ax = plt.subplots(figsize=(10, 5.5), facecolor='#1e293b')
    ax.set_facecolor('#0f172a')
    
    # Truncate location titles for clean visual labels
    labels = [p[:35] + '...' if len(p) > 35 else p for p in top10_df['place']]
    mags = top10_df['magnitude'].values
    
    # Color gradient based on magnitude strength
    colors = ['#f43f5e' if m >= 5.0 else '#f59e0b' if m >= 3.5 else '#38bdf8' for m in mags]
    
    bars = ax.barh(labels, mags, color=colors, height=0.6, edgecolor='none')
    
    ax.set_title('Top 10 Strongest Earthquakes (Past 7 Days)', fontsize=14, fontweight='bold', pad=15, color='#f8fafc')
    ax.set_xlabel('Magnitude (M)', fontsize=11, color='#94a3b8', labelpad=10)
    ax.grid(True, linestyle='--', alpha=0.2, color='#ffffff', axis='x')
    ax.tick_params(colors='#94a3b8')
    
    # Value labels at the end of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}', ha='left', va='center', color='#f8fafc', fontweight='bold')

    ax.set_xlim(0, max(mags) + 1.0)
    plt.tight_layout()
    bar_chart_path = os.path.join(CHARTS_DIR, 'top10_strongest.png')
    plt.savefig(bar_chart_path, dpi=120)
    plt.close()

    return {
        "line_chart": "/static/charts/daily_occurrences.png",
        "bar_chart": "/static/charts/top10_strongest.png"
    }

def get_top_earthquakes(df, n=10):
    """Returns top N strongest earthquakes formatted for dashboard presentation."""
    if df.empty:
        return []
    
    top_df = df.sort_values('magnitude', ascending=False).head(n)
    return top_df.to_dict(orient='records')

def generate_summary(df):
    """Generates an executive textual summary of recent seismic activity."""
    stats = calculate_statistics(df)
    ts = calculate_time_series(df)
    
    if df.empty:
        return "No earthquake data available for the past 7 days."
        
    top_eq = df.sort_values('magnitude', ascending=False).iloc[0]
    major_count = len(df[df['magnitude'] >= 5.0])
    
    observations = [
        f"A total of {stats['total_count']} earthquakes were recorded globally over the past 7 days.",
        f"The mean seismic magnitude was {stats['mean_magnitude']} M with a median of {stats['median_magnitude']} M (Std Dev: {stats['std_dev']}).",
        f"The highest seismic activity occurred on {ts['peak_day']} with {ts['peak_count']} recorded earthquakes.",
        f"The strongest earthquake was {top_eq['title']} recorded at {top_eq['formatted_time']}."
    ]
    
    if major_count > 0:
        observations.append(f"A total of {major_count} significant seismic events (Magnitude ≥ 5.0) were registered.")
    else:
        observations.append("No major earthquakes exceeding Magnitude 5.0 were recorded during this period.")
        
    return observations
