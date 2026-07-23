from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from predictor.models import Disease
from history.models import PredictionHistory

class PredictorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='SafePass123_!')
        self.disease = Disease.objects.create(
            name="Fungal infection",
            description="A fungal infection is an inflammatory condition.",
            causes="Fungi growth.",
            precautions="bath twice, use dettol, keep dry, clean area",
            specialist="Dermatologist"
        )

    def test_public_pages_status_code_and_context(self):
        for url_name in ['home', 'about', 'contact']:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context.get('is_public_page'))

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'John Doe',
            'email': 'john@example.com',
            'subject': 'Support Request',
            'message': 'Hello, I need help with the classifier.'
        })
        self.assertRedirects(response, reverse('contact'))
        # Check email was simulated/sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("MediPredict AI Contact Form: Support Request", mail.outbox[0].subject)

    def test_predict_disease_view_get(self):
        self.client.login(username='testuser', password='SafePass123_!')
        response = self.client.get(reverse('predict_disease'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "itching")

    def test_predict_disease_view_post_success(self):
        self.client.login(username='testuser', password='SafePass123_!')
        # Post some symptoms matching Fungal infection
        response = self.client.post(reverse('predict_disease'), {
            'symptoms': ['itching', 'skin_rash', 'nodal_skin_eruptions', 'dischromic_patches']
        })
        # Should redirect to prediction_result
        self.assertEqual(response.status_code, 302)
        history_record = PredictionHistory.objects.first()
        self.assertIsNotNone(history_record)
        self.assertEqual(history_record.user, self.user)
        self.assertIn("itching", history_record.symptoms)

    def test_predict_disease_view_post_empty_symptoms(self):
        self.client.login(username='testuser', password='SafePass123_!')
        response = self.client.post(reverse('predict_disease'), {
            'symptoms': []
        })
        self.assertRedirects(response, reverse('predict_disease'))

    def test_bmi_calculator_anonymous(self):
        response = self.client.get(reverse('bmi_calculator'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(reverse('bmi_calculator'), {
            'height': 180.0,
            'weight': 75.0
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "23.15") # BMI value
        self.assertContains(response, "Normal Weight")

    def test_bmi_calculator_authenticated_saves_to_profile(self):
        self.client.login(username='testuser', password='SafePass123_!')
        response = self.client.post(reverse('bmi_calculator'), {
            'height': 175.0,
            'weight': 80.0
        })
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.height_cm, 175.0)
        self.assertEqual(self.user.profile.weight_kg, 80.0)
