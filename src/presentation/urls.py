
from django.urls import path
from presentation.views import index


urlpatterns = [
    path('', index, name="home")
]