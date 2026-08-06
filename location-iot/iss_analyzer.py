import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

def analyze_iss_data(csv_path="iss_location_data.csv", output_dir="."):
    """
    Analyzes ISS location data CSV, prints statistical metrics,
    and generates high-resolution plot images.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Data file '{csv_path}' not found.")
        
    df = pd.read_csv(csv_path)
    df["Timestamp_dt"] = pd.to_datetime(df["Timestamp"])
    
    # Calculate Statistical Metrics
    max_lat = df["Latitude"].max()
    min_lat = df["Latitude"].min()
    avg_lat = df["Latitude"].mean()
    
    max_lon = df["Longitude"].max()
    min_lon = df["Longitude"].min()
    avg_lon = df["Longitude"].mean()
    
    metrics = {
        "max_lat": max_lat,
        "min_lat": min_lat,
        "avg_lat": avg_lat,
        "max_lon": max_lon,
        "min_lon": min_lon,
        "avg_lon": avg_lon,
        "count": len(df)
    }
    
    print("==================================================")
    print("            ISS LOCATION DATA ANALYSIS            ")
    print("==================================================")
    print(f"Total Samples Collected: {len(df)}")
    print("--- Latitude Statistics ---")
    print(f"  Maximum Latitude : {max_lat:8.4f}°")
    print(f"  Minimum Latitude : {min_lat:8.4f}°")
    print(f"  Average Latitude : {avg_lat:8.4f}°")
    print("--- Longitude Statistics ---")
    print(f"  Maximum Longitude: {max_lon:8.4f}°")
    print(f"  Minimum Longitude: {min_lon:8.4f}°")
    print(f"  Average Longitude: {avg_lon:8.4f}°")
    print("==================================================")

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # 1. Plot Latitude vs Time
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.plot(df["Timestamp_dt"], df["Latitude"], color="#1f77b4", linewidth=2.5, marker="o", markersize=3, label="Latitude (°)")
    ax.set_title("ISS Latitude vs. Time", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Time (HH:MM:SS)", fontsize=12, labelpad=10)
    ax.set_ylabel("Latitude (Degrees)", fontsize=12, labelpad=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left")
    plt.tight_layout()
    lat_plot_path = os.path.join(output_dir, "latitude_vs_time.png")
    plt.savefig(lat_plot_path)
    plt.close()

    # 2. Plot Longitude vs Time
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.plot(df["Timestamp_dt"], df["Longitude"], color="#ff7f0e", linewidth=2.5, marker="o", markersize=3, label="Longitude (°)")
    ax.set_title("ISS Longitude vs. Time", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Time (HH:MM:SS)", fontsize=12, labelpad=10)
    ax.set_ylabel("Longitude (Degrees)", fontsize=12, labelpad=10)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    fig.autofmt_xdate()
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left")
    plt.tight_layout()
    lon_plot_path = os.path.join(output_dir, "longitude_vs_time.png")
    plt.savefig(lon_plot_path)
    plt.close()

    # 3. Plot 2D ISS Ground Trajectory Map (Latitude vs Longitude)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.plot(df["Longitude"], df["Latitude"], color="#2ca02c", linewidth=2.5, label="Flight Path")
    ax.scatter(df["Longitude"].iloc[0], df["Latitude"].iloc[0], color="#d62728", s=100, zorder=5, label="Start Point")
    ax.scatter(df["Longitude"].iloc[-1], df["Latitude"].iloc[-1], color="#9467bd", s=100, zorder=5, label="End Point")
    ax.set_title("ISS Ground Trajectory (Latitude vs Longitude)", fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Longitude (Degrees)", fontsize=12, labelpad=10)
    ax.set_ylabel("Latitude (Degrees)", fontsize=12, labelpad=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="best")
    plt.tight_layout()
    traj_plot_path = os.path.join(output_dir, "iss_trajectory_map.png")
    plt.savefig(traj_plot_path)
    plt.close()

    print(f"\nGenerated Plots:")
    print(f" - {lat_plot_path}")
    print(f" - {lon_plot_path}")
    print(f" - {traj_plot_path}")

    return metrics

if __name__ == "__main__":
    analyze_iss_data()
