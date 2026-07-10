from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import csv

# Import database module from project root
import database

def auto_create_admin(**kwargs):
    """Auto-creates a default admin user if one doesn't already exist."""
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
            print("Auto-created default superuser: admin / admin123")
    except Exception as e:
        print(f"Failed to auto-create superuser: {e}")

def login_view(request):
    """Handles user sign in and displays login form."""
    if request.user.is_authenticated:
        return redirect("dashboard")
        
    error_message = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            error_message = "Invalid username or password."
            
    return render(request, "dashboard/login.html", {"error_message": error_message})

def logout_view(request):
    """Logs out the user and redirects to login."""
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def dashboard_view(request):
    """Renders the main dashboard page."""
    context = {
        "use_supabase": database.use_supabase
    }
    return render(request, "dashboard/index.html", context)

@login_required(login_url="login")
def api_readings(request):
    """
    API endpoint that returns temperature records as JSON.
    Supports filtering by start_date and end_date.
    """
    start_date = request.GET.get("start_date") or None
    end_date = request.GET.get("end_date") or None
    
    # Clean filters
    if start_date == "":
        start_date = None
    if end_date == "":
        end_date = None
        
    readings = database.get_readings(start_date=start_date, end_date=end_date)
    
    # Calculate statistics
    temperatures = [r["temperature"] for r in readings]
    stats = {
        "latest": temperatures[0] if temperatures else None,
        "avg": round(sum(temperatures) / len(temperatures), 1) if temperatures else None,
        "min": min(temperatures) if temperatures else None,
        "max": max(temperatures) if temperatures else None,
        "count": len(temperatures)
    }
    
    # Add a formatted time string if latest exists
    if stats["latest"] is not None:
        stats["latest_time"] = f"{readings[0]['date']} {readings[0]['time']}"
    else:
        stats["latest_time"] = "No Data"
        
    return JsonResponse({
        "status": "success",
        "stats": stats,
        "readings": readings # Sent in descending order of timestamp
    })

@login_required(login_url="login")
def export_csv(request):
    """
    API endpoint that exports filtered temperature records as a CSV file.
    """
    start_date = request.GET.get("start_date") or None
    end_date = request.GET.get("end_date") or None
    
    # Clean filters
    if start_date == "":
        start_date = None
    if end_date == "":
        end_date = None
        
    readings = database.get_readings(start_date=start_date, end_date=end_date)
    
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    filename = f"temperature_readings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(["ID", "Temperature (°C)", "Date", "Time (Timestamp)", "Epoch Timestamp"])
    
    for row in readings:
        writer.writerow([
            row["id"],
            row["temperature"],
            row["date"],
            row["time"],
            row["timestamp"]
        ])
        
    return response
