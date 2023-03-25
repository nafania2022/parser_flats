from django.shortcuts import render
from django.views.generic import ListView
from .models import *


# Create your views here.
class Home(ListView):
    model = Flats
    paginate_by = 5 
    template_name = "flats_publ/home.html"
    context_object_name = "flats"
    
    
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"  
        context["cities"] = Cities.objects.all()      
        return context
    
class ShowFilteCity(ListView):
    model = Flats
    slug_url_kwarg = 'sort_city'
    paginate_by = 5 
    template_name = "flats_publ/city_flats.html"
    context_object_name = "flats"
    
    def get_queryset(self):
        return Flats.objects.filter(city=self.kwargs['sort_city'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = Cities.objects.all()
                
        return context
    