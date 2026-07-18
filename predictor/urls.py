from django.urls import path
from .views import HomeView, AboutView, ContactView, PredictDiseaseView, PredictionResultView, BMICalculatorView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('predict/', PredictDiseaseView.as_view(), name='predict_disease'),
    path('result/<int:history_id>/', PredictionResultView.as_view(), name='prediction_result'),
    path('bmi/', BMICalculatorView.as_view(), name='bmi_calculator'),
]
