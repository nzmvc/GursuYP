from django.contrib import admin
from django.urls import path
from . import views

app_name="workflow"

urlpatterns = [
    path('workflowList/', views.workflowList, name='workflowList'),

    
    
]