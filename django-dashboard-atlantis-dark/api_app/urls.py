from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.login_user),
    path('api/projects/<int:pk>', views.ProjectsApiView.as_view()),
]