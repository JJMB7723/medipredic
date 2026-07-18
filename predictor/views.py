import os
import pickle
import json
import numpy as np
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .models import Disease
from .forms import ContactForm, BMIForm
from medicines.models import Medicine
from history.models import PredictionHistory

# Function to ensure ML model is trained and available
def get_ml_model_and_symptoms():
    model_dir = os.path.join(settings.BASE_DIR, 'predictor', 'ml_models')
    model_path = os.path.join(model_dir, 'disease_predictor_model.pkl')
    symptoms_path = os.path.join(model_dir, 'symptoms_list.json')

    try:
        # If files don't exist, train the model automatically
        if not os.path.exists(model_path) or not os.path.exists(symptoms_path):
            print("[*] ML model files not found. Auto-training classifier...")
            # Inline import to avoid circular dependency issues
            from train_model import download_or_generate_datasets, train_and_save_model
            download_or_generate_datasets()
            train_and_save_model()

        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        with open(symptoms_path, 'r') as f:
            symptoms_list = json.load(f)

        return model, symptoms_list
    except Exception as e:
        print(f"[!] Failed to load pickle ML model ({e}). Using pure-python high-fidelity fallback classifier.")
        from .fallback_model import FallbackDiseaseClassifier, SYMPTOMS_LIST
        return FallbackDiseaseClassifier(), SYMPTOMS_LIST

class HomeView(TemplateView):
    template_name = 'predictor/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add basic health tips
        context['health_tips'] = [
            {"title": "Stay Hydrated", "text": "Drink at least 8-10 glasses of water daily to flush out toxins and keep your body energized.", "icon": "fa-droplet"},
            {"title": "Get Quality Sleep", "text": "7-8 hours of sound sleep helps repair cells, boost immunity, and improve cognitive performance.", "icon": "fa-bed"},
            {"title": "Regular Exercise", "text": "Engage in 30 minutes of physical activity like walking or jogging to keep your heart healthy.", "icon": "fa-heart-pulse"},
            {"title": "Balanced Nutrition", "text": "Incorporate green leafy vegetables, fresh fruits, proteins, and whole grains into your meals.", "icon": "fa-apple-whole"},
        ]
        return context

class AboutView(TemplateView):
    template_name = 'predictor/about.html'

class ContactView(FormView):
    form_class = ContactForm
    template_name = 'predictor/contact.html'
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']

        # Send email log
        try:
            send_mail(
                subject=f"MediPredict AI Contact Form: {subject}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(self.request, "Thank you for contacting us! We have received your message and will get back to you shortly.")
        except Exception as e:
            messages.warning(self.request, f"Your inquiry was registered, but email transmission failed. Ref: {e}")
        
        return super().form_valid(form)

class PredictDiseaseView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            _, symptoms_list = get_ml_model_and_symptoms()
        except Exception as e:
            messages.error(request, f"Error initializing predictor model: {e}")
            symptoms_list = []

        # Convert snake_case symptom names to readable text for multi-select checkboxes
        formatted_symptoms = []
        for sym in symptoms_list:
            formatted_symptoms.append({
                'value': sym,
                'name': sym.replace('_', ' ').strip().capitalize()
            })

        # Sort formatted symptoms alphabetically for better UX
        formatted_symptoms = sorted(formatted_symptoms, key=lambda k: k['name'])

        return render(request, 'predictor/predict_disease.html', {
            'symptoms': formatted_symptoms
        })

    def post(self, request):
        selected_symptoms = request.POST.getlist('symptoms')
        
        if not selected_symptoms:
            messages.error(request, "Please select at least 2 or 3 symptoms to make a prediction.")
            return redirect('predict_disease')

        try:
            model, symptoms_list = get_ml_model_and_symptoms()
            
            # Prepare prediction input vector
            input_vector = [0] * len(symptoms_list)
            for sym in selected_symptoms:
                if sym in symptoms_list:
                    idx = symptoms_list.index(sym)
                    input_vector[idx] = 1

            # Perform prediction
            features = np.array([input_vector])
            prediction = model.predict(features)[0]
            
            # Calculate confidence score
            probabilities = model.predict_proba(features)[0]
            class_indices = model.classes_
            
            # Match predicted class probability
            confidence_score = 0.0
            for idx, label in enumerate(class_indices):
                if label.strip() == prediction.strip():
                    confidence_score = float(probabilities[idx]) * 100
                    break

            if confidence_score == 0.0:
                # Fallback in case of exact match issues
                confidence_score = float(max(probabilities)) * 100

            # Query disease information from database
            clean_prediction_name = prediction.strip()
            disease_instance = Disease.objects.filter(name__iexact=clean_prediction_name).first()

            # Retrieve recommended medications
            medicines_str = ""
            if disease_instance:
                medicines = Medicine.objects.filter(disease=disease_instance)
                medicines_str = ", ".join([m.medicine_name for m in medicines])
            else:
                medicines_str = "Consult a Doctor"

            # Create prediction history log
            history_record = PredictionHistory.objects.create(
                user=request.user,
                symptoms=",".join(selected_symptoms),
                predicted_disease=clean_prediction_name,
                confidence_score=round(confidence_score, 2),
                medicines=medicines_str
            )

            # Redirect to prediction results detail page (which is the history detail page)
            return redirect('prediction_result', history_id=history_record.id)

        except Exception as e:
            messages.error(request, f"An error occurred during prediction calculations: {e}")
            return redirect('predict_disease')

class PredictionResultView(LoginRequiredMixin, View):
    def get(self, request, history_id):
        # Fetch the historical prediction record
        history = get_object_or_404(PredictionHistory, id=history_id, user=request.user)
        
        # Get matching disease from database
        disease = Disease.objects.filter(name__iexact=history.predicted_disease.strip()).first()
        
        medicines = []
        if disease:
            medicines = Medicine.objects.filter(disease=disease)
            
        # Parse symptoms list for rendering
        symptoms_list = history.get_symptoms_list()

        # Emergency warnings indicator (mocked flags based on critical symptoms in vector)
        critical_symptoms = [
            'chest_pain', 'breathlessness', 'coma', 'stomach_bleeding', 
            'altered_sensorium', 'acute_liver_failure', 'weakness_of_one_body_side'
        ]
        has_critical_symptoms = any(cs in history.symptoms.split(',') for cs in critical_symptoms)

        return render(request, 'predictor/prediction_results.html', {
            'history': history,
            'disease': disease,
            'medicines': medicines,
            'symptoms_list': symptoms_list,
            'has_critical_symptoms': has_critical_symptoms
        })

class BMICalculatorView(View):
    def get(self, request):
        # If user is authenticated, we pre-fill from profile
        initial_data = {}
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile:
                if profile.height_cm:
                    initial_data['height'] = profile.height_cm
                if profile.weight_kg:
                    initial_data['weight'] = profile.weight_kg
                    
        form = BMIForm(initial=initial_data)
        return render(request, 'predictor/bmi_calculator.html', {'form': form})

    def post(self, request):
        form = BMIForm(request.POST)
        if form.is_valid():
            height_cm = form.cleaned_data['height']
            weight_kg = form.cleaned_data['weight']
            
            # BMI Calculation: kg / m^2
            height_m = height_cm / 100.0
            bmi = weight_kg / (height_m ** 2)
            bmi = round(bmi, 2)
            
            # Classification
            category = ""
            css_class = ""
            advice = ""
            
            if bmi < 18.5:
                category = "Underweight"
                css_class = "bmi-underweight"
                advice = "It is recommended to consume more calorie-dense whole foods and consult a nutritionist to safely build healthy muscle mass."
            elif 18.5 <= bmi < 25.0:
                category = "Normal Weight"
                css_class = "bmi-normal"
                advice = "Great job! Keep maintaining your healthy lifestyle with regular exercise and a well-balanced diet."
            elif 25.0 <= bmi < 30.0:
                category = "Overweight"
                css_class = "bmi-overweight"
                advice = "Consider reducing intake of refined sugars and increasing cardio workouts to return to a normal range."
            else:
                category = "Obese"
                css_class = "bmi-obese"
                advice = "We strongly suggest contacting a healthcare specialist or dietary consultant to outline a structured physical exercise and diet plan."

            # If user is authenticated, we can automatically update their profile values
            if request.user.is_authenticated:
                profile = getattr(request.user, 'profile', None)
                if profile:
                    profile.height_cm = height_cm
                    profile.weight_kg = weight_kg
                    profile.save()
                    messages.success(request, "BMI details saved to your profile profile!")

            return render(request, 'predictor/bmi_calculator.html', {
                'form': form,
                'bmi': bmi,
                'category': category,
                'css_class': css_class,
                'advice': advice,
                'height': height_cm,
                'weight': weight_kg
            })
            
        return render(request, 'predictor/bmi_calculator.html', {'form': form})
