from django.contrib import admin
from django.urls import path
from . import views

app_name="user"

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('userAdd/', views.userAdd, name='userAdd'),
    path('userList/', views.userList, name='userList'),
    path('userView/<int:id>', views.userView, name='userView'),
    path('userUpdate/<int:id>', views.userUpdate, name='userUpdate'),
    path('userDelete/<int:id>', views.userDelete, name='userDelete'),
    path('userChangePassword/<int:id>', views.userChangePassword, name='userChangePassword'),
    path('logView/', views.logView, name='logView'),
    path('yetkiYok/', views.yetkiYok, name='yetkiYok'),
    
    
]
