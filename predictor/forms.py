from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Your Full Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Your Email Address'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Message Subject'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Type your message here...', 'rows': 5
    }))

class BMIForm(forms.Form):
    weight = forms.FloatField(min_value=1.0, max_value=500.0, label="Weight (kg)", widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. 70', 'step': '0.1'
    }))
    height = forms.FloatField(min_value=1.0, max_value=300.0, label="Height (cm)", widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g. 175', 'step': '0.1'
    }))
