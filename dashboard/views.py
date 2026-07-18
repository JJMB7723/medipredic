import csv
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from history.models import PredictionHistory
from predictor.models import Disease
from medicines.models import Medicine
from django.db.models import Count

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/user_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # User predictions history
        user_predictions = PredictionHistory.objects.filter(user=user)
        total_predictions = user_predictions.count()
        recent_predictions = user_predictions[:5] if total_predictions > 0 else []
        
        # Consolidate medicines history from predictions
        medicine_history = []
        for pred in user_predictions:
            if pred.medicines:
                # split medications
                meds = [m.strip() for m in pred.medicines.split(',') if m.strip()]
                for med in meds:
                    if med not in medicine_history:
                        medicine_history.append(med)
                        
        # Health advice based on prediction trends
        recommendations = []
        if total_predictions > 0:
            latest_pred = user_predictions.first()
            disease_name = latest_pred.predicted_disease
            disease_obj = Disease.objects.filter(name__iexact=disease_name).first()
            if disease_obj:
                recommendations = disease_obj.get_precautions_list()[:3]
        
        context.update({
            'total_predictions': total_predictions,
            'recent_predictions': recent_predictions,
            'medicine_history': medicine_history[:6],
            'recommendations': recommendations,
            'last_login': user.last_login,
        })
        return context

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # System-wide counts
        total_users = User.objects.count()
        total_diseases = Disease.objects.count()
        total_medicines = Medicine.objects.count()
        total_predictions = PredictionHistory.objects.count()
        
        # Analytics: Top Predicted Diseases
        top_diseases = PredictionHistory.objects.values('predicted_disease').annotate(
            count=Count('predicted_disease')
        ).order_by('-count')[:5]
        
        # List of system users
        users = User.objects.all().order_by('-date_joined')[:10]
        
        # Recent predictions across the entire system
        system_predictions = PredictionHistory.objects.select_related('user').all().order_by('-created_at')[:10]
        
        context.update({
            'total_users': total_users,
            'total_diseases': total_diseases,
            'total_medicines': total_medicines,
            'total_predictions': total_predictions,
            'top_diseases': top_diseases,
            'users': users,
            'system_predictions': system_predictions,
        })
        return context

class ExportAnalyticsCSVView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="medipredict_analytics.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Prediction ID', 'User', 'User Email', 'Symptoms Entered', 'Predicted Disease', 'Confidence Score %', 'Medications Prescribed', 'Date Created'])
        
        predictions = PredictionHistory.objects.select_related('user').all().order_by('-created_at')
        for pred in predictions:
            writer.writerow([
                pred.id,
                pred.user.username,
                pred.user.email,
                pred.symptoms,
                pred.predicted_disease,
                pred.confidence_score,
                pred.medicines,
                pred.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')
            ])
            
        return response
