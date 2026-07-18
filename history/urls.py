from django.urls import path
from .views import PredictionHistoryListView, DeletePredictionHistoryView, DownloadPredictionPDFView

urlpatterns = [
    path('', PredictionHistoryListView.as_view(), name='prediction_history'),
    path('delete/<int:history_id>/', DeletePredictionHistoryView.as_view(), name='delete_history'),
    path('download/<int:history_id>/', DownloadPredictionPDFView.as_view(), name='download_history_pdf'),
]
