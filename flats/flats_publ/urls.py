
from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<str:sort_city>', ShowFilteCity.as_view(), name='filter_city'),
    
]
