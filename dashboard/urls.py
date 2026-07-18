from django.urls import path
from .views import UserDashboardView, AdminDashboardView, ExportAnalyticsCSVView

urlpatterns = [
    path('', UserDashboardView.as_view(), name='dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('export/', ExportAnalyticsCSVView.as_view(), name='export_analytics'),
]
