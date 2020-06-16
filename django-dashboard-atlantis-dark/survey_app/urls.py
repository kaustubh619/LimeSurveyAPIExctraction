from django.urls import path
from . import views

urlpatterns = [
    path('survey', views.survey),
    path("get_data", views.GetData.as_view()),
]