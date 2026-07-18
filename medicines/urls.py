from django.urls import path
from .views import MedicineListView, MedicineDetailView

urlpatterns = [
    path('', MedicineListView.as_view(), name='medicine_list'),
    path('<int:pk>/', MedicineDetailView.as_view(), name='medicine_detail'),
]
