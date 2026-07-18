from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medicine

class MedicineListView(LoginRequiredMixin, ListView):
    model = Medicine
    template_name = 'medicines/medicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Medicine.objects.filter(medicine_name__icontains=query)
        return Medicine.objects.all()

class MedicineDetailView(LoginRequiredMixin, DetailView):
    model = Medicine
    template_name = 'medicines/medicine_detail.html'
    context_object_name = 'medicine'
