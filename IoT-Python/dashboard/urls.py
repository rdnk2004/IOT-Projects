from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/readings/', views.api_readings, name='api_readings'),
    path('api/export/', views.export_csv, name='export_csv'),
]
