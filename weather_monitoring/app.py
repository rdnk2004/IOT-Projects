from datetime import date
from flask import Flask, render_template, jsonify, request
import config
import database
import fetcher
import analytics
import seed_data

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Initialize database schema and start background scheduler
database.init_db()

# Backfill initial 24h data if database is fresh
try:
    if not database.get_latest_reading():
        seed_data.seed_past_24h_data()
except Exception as e:
    print(f"Initial seed check notice: {e}")

# Start background weather fetcher scheduler (5-minute interval)
fetcher.start_weather_scheduler()


@app.route('/')
def index():
    """Live Weather Dashboard View with Matplotlib Time Series Chart."""
    latest = database.get_latest_reading()
    # Generate fresh Matplotlib time series visualization
    analytics.generate_matplotlib_weather_charts()
    return render_template('index.html', latest=latest)


@app.route('/analytics')
def analytics_view():
    """Statistical & Time Series Analysis View with Matplotlib Charts."""
    selected_date = request.args.get('date', str(date.today()))
    stats_data = analytics.calculate_daily_statistics(selected_date)
    ts_data = analytics.calculate_time_series_analysis(selected_date)
    # Generate fresh Matplotlib hourly breakdown visualization
    charts = analytics.generate_matplotlib_weather_charts(selected_date)
    return render_template('analytics.html', stats=stats_data, ts=ts_data, selected_date=selected_date, charts=charts)


@app.route('/report')
def report_view():
    """Daily Summary Report View."""
    selected_date = request.args.get('date', str(date.today()))
    report_data = analytics.generate_daily_report(selected_date)
    return render_template('report.html', report=report_data, selected_date=selected_date)


# REST API Endpoints

@app.route('/api/current')
def api_current():
    """Returns latest current weather reading."""
    reading = database.get_latest_reading()
    if not reading:
        reading = fetcher.fetch_kochi_weather()
    return jsonify({"status": "success", "data": reading})


@app.route('/api/history')
def api_history():
    """Returns temperature reading history."""
    limit = request.args.get('limit', default=100, type=int)
    readings = database.get_readings_range(limit=limit)
    return jsonify({"status": "success", "count": len(readings), "data": readings})


@app.route('/api/stats')
def api_stats():
    """Returns statistical analysis metrics."""
    target_date = request.args.get('date', None)
    stats_data = analytics.calculate_daily_statistics(target_date)
    return jsonify({"status": "success", "data": stats_data})


@app.route('/api/timeseries')
def api_timeseries():
    """Returns time series analysis and hourly averages."""
    target_date = request.args.get('date', None)
    ts_data = analytics.calculate_time_series_analysis(target_date)
    return jsonify({"status": "success", "data": ts_data})


@app.route('/api/report')
def api_report():
    """Returns complete daily summary report payload."""
    target_date = request.args.get('date', None)
    report_data = analytics.generate_daily_report(target_date)
    return jsonify({"status": "success", "data": report_data})


@app.route('/api/trigger-fetch', methods=['POST'])
def api_trigger_fetch():
    """Manually triggers an immediate weather fetch from Open-Meteo and updates Matplotlib charts."""
    reading = fetcher.fetch_kochi_weather()
    analytics.generate_matplotlib_weather_charts()
    if reading:
        return jsonify({"status": "success", "message": "Weather data retrieved and saved.", "data": reading})
    else:
        return jsonify({"status": "error", "message": "Failed to retrieve weather data from Open-Meteo."}), 500


if __name__ == '__main__':
    print(f"Starting Kochi IoT Weather Monitoring Server on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
