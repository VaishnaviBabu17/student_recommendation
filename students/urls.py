from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('create-admin/', views.create_admin),
]
