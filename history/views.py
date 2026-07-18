import io
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse

from .models import PredictionHistory
from predictor.models import Disease

# ReportLab Imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PredictionHistoryListView(LoginRequiredMixin, ListView):
    model = PredictionHistory
    template_name = 'history/prediction_history.html'
    context_object_name = 'histories'
    paginate_by = 15

    def get_queryset(self):
        # Only show history of current user
        queryset = PredictionHistory.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                predicted_disease__icontains=query
            ) | queryset.filter(
                symptoms__icontains=query
            )
        return queryset

class DeletePredictionHistoryView(LoginRequiredMixin, View):
    def post(self, request, history_id):
        history = get_object_or_404(PredictionHistory, id=history_id, user=request.user)
        disease_name = history.predicted_disease
        history.delete()
        messages.success(request, f"Prediction report for {disease_name} has been deleted.")
        return redirect('prediction_history')

class DownloadPredictionPDFView(LoginRequiredMixin, View):
    def get(self, request, history_id):
        # Fetch target prediction log
        history = get_object_or_404(PredictionHistory, id=history_id, user=request.user)
        
        # Get matching disease from database
        disease = Disease.objects.filter(name__iexact=history.predicted_disease.strip()).first()
        
        # Setup bytes buffer for PDF output
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=54,
            leftMargin=54,
            topMargin=54,
            bottomMargin=72
        )
        
        # Base styles
        styles = getSampleStyleSheet()
        
        # Custom palette
        primary_color = colors.HexColor('#0d9488')   # Teal
        text_color = colors.HexColor('#1f2937')      # Slate 800
        secondary_color = colors.HexColor('#4b5563') # Slate 600
        accent_color = colors.HexColor('#e11d48')    # Red alert
        bg_light = colors.HexColor('#f3f4f6')        # Light grey
        
        # Custom Typography Styles
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=24,
            leading=28,
            textColor=primary_color,
            spaceAfter=15
        )
        
        h1_style = ParagraphStyle(
            'H1Style',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=primary_color,
            spaceBefore=15,
            spaceAfter=8,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'BodyTextCustom',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=text_color,
            spaceAfter=6
        )
        
        meta_label_style = ParagraphStyle(
            'MetaLabel',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=primary_color
        )
        
        disclaimer_style = ParagraphStyle(
            'DisclaimerText',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=11,
            textColor=secondary_color,
            alignment=1 # Center
        )
        
        story = []
        
        # Header banner
        story.append(Paragraph("MediPredict AI — Medical Diagnosis Report", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=primary_color, spaceBefore=1, spaceAfter=15))
        
        # Metadata Table (Patient details & Date)
        meta_data = [
            [
                Paragraph("Patient Name:", meta_label_style),
                Paragraph(f"{request.user.first_name} {request.user.last_name} ({request.user.username})", body_style),
                Paragraph("Date & Time:", meta_label_style),
                Paragraph(history.created_at.strftime('%Y-%m-%d %H:%M:%S UTC'), body_style)
            ],
            [
                Paragraph("Predicted Condition:", meta_label_style),
                Paragraph(f"<b>{history.predicted_disease}</b>", body_style),
                Paragraph("Confidence level:", meta_label_style),
                Paragraph(f"<b>{history.confidence_score}%</b>", body_style)
            ]
        ]
        
        meta_table = Table(meta_data, colWidths=[120, 180, 100, 104])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_light),
            ('PADDING', (0,0), (-1,-1), 8),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 15))
        
        # Symptoms List
        story.append(Paragraph("Reported Symptoms", h1_style))
        symptoms_str = ", ".join(history.get_symptoms_list())
        story.append(Paragraph(symptoms_str, body_style))
        story.append(Spacer(1, 10))
        
        # Disease details
        if disease:
            # Description
            story.append(Paragraph("Disease Description", h1_style))
            story.append(Paragraph(disease.description, body_style))
            
            # Causes
            story.append(Paragraph("Possible Causes", h1_style))
            story.append(Paragraph(disease.causes, body_style))
            
            # Precautions
            story.append(Paragraph("Recommended Precautions", h1_style))
            precautions_list = disease.get_precautions_list()
            for idx, prec in enumerate(precautions_list, 1):
                story.append(Paragraph(f"<b>{idx}.</b> {prec.capitalize()}", body_style))
                
            # Specialist Care
            story.append(Spacer(1, 10))
            story.append(Paragraph("Suggested Specialist Doctor", h1_style))
            story.append(Paragraph(f"Consult an specialist in: <b>{disease.specialist}</b>", body_style))
        else:
            story.append(Paragraph("Disease Details", h1_style))
            story.append(Paragraph("No supplementary disease lookup details found in the database. Please contact your administrator.", body_style))
            
        # Medications
        story.append(Paragraph("Commonly Used Medications", h1_style))
        if history.medicines:
            story.append(Paragraph(history.medicines, body_style))
        else:
            story.append(Paragraph("No registered medication details available.", body_style))
            
        story.append(Spacer(1, 30))
        
        # Disclaimer Card
        disclaimer_text = (
            "<b>DISCLAIMER:</b> This application is for educational purposes only and should not be considered "
            "professional medical advice. Consult a qualified healthcare professional before taking any medication."
        )
        disclaimer_data = [[Paragraph(disclaimer_text, disclaimer_style)]]
        disclaimer_table = Table(disclaimer_data, colWidths=[504])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#fee2e2')),
            ('PADDING', (0,0), (-1,-1), 12),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LINELEFT', (0,0), (0,-1), 3, accent_color),
        ]))
        story.append(disclaimer_table)
        
        # Build Document
        def add_footer(canvas, doc):
            canvas.saveState()
            canvas.setFont('Helvetica', 8)
            canvas.setFillColor(secondary_color)
            canvas.drawString(54, 30, "MediPredict AI Medical Systems Inc.")
            canvas.drawRightString(doc.pagesize[0] - 54, 30, f"Page {doc.page}")
            canvas.restoreState()
            
        doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
        
        # Return PDF via HTTP Response
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="MediPredict_Report_{history.id}.pdf"'
        response.write(pdf)
        return response
