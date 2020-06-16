from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects1'),
    path('projects', views.projects, name='projects'),
    path('create_project', views.create_project, name='create_project'),
    path('addcard/', views.addCard, name='addcard'),
    path('create_org', views.CreateOrg.as_view({'get': 'list'})),
    path('create_proj', views.CreateProj.as_view({'get': 'list'})),
    path('subscribe/<int:pk>', views.ProjectSubscription.as_view()),

    path('postdetails/<int:pk>/', views.postMEdetails, name = "postdetails"),
    path("payment_redirect", views.payment_redirect)
]