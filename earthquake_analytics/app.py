from flask import Flask, render_template, jsonify, request
import analytics
import fetcher

app = Flask(__name__)
app.config['SECRET_KEY'] = 'earthquake_analytics_usgs_secret_2026'

# Global cached dataframe
cached_df = None

def get_or_update_df(force=False):
    global cached_df
    if cached_df is None or force or cached_df.empty:
        records = fetcher.fetch_usgs_earthquake_data()
        cached_df = analytics.process_earthquake_dataframe(records)
        if not cached_df.empty:
            analytics.generate_visualizations(cached_df)
    return cached_df


@app.route('/')
def index():
    """Main USGS Earthquake Analytics Dashboard View."""
    df = get_or_update_df()
    stats = analytics.calculate_statistics(df)
    ts = analytics.calculate_time_series(df)
    top10 = analytics.get_top_earthquakes(df, 10)
    summary = analytics.generate_summary(df)
    
    return render_template(
        'index.html',
        stats=stats,
        ts=ts,
        top10=top10,
        summary=summary
    )


@app.route('/api/stats')
def api_stats():
    """Returns calculated magnitude statistical metrics."""
    df = get_or_update_df()
    stats = analytics.calculate_statistics(df)
    return jsonify({"status": "success", "data": stats})


@app.route('/api/timeseries')
def api_timeseries():
    """Returns time series analysis and peak activity day."""
    df = get_or_update_df()
    ts = analytics.calculate_time_series(df)
    return jsonify({"status": "success", "data": ts})


@app.route('/api/top')
def api_top():
    """Returns top N strongest earthquakes."""
    limit = request.args.get('limit', default=10, type=int)
    df = get_or_update_df()
    top_eqs = analytics.get_top_earthquakes(df, limit)
    return jsonify({"status": "success", "count": len(top_eqs), "data": top_eqs})


@app.route('/api/refresh', methods=['POST'])
def api_refresh():
    """Refreshes USGS data feed and re-generates Matplotlib visualizations."""
    df = get_or_update_df(force=True)
    return jsonify({"status": "success", "message": f"Successfully updated telemetry with {len(df)} earthquakes."})


if __name__ == '__main__':
    print("Starting USGS Earthquake Analytics Dashboard on http://127.0.0.1:5001 ...")
    app.run(host='0.0.0.0', port=5001, debug=True)
