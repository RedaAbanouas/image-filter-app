from django.urls import path
from pipeline.views import home

urlpatterns = [path("", home, name="home")]
