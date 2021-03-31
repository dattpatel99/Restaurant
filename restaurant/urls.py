from django.contrib import admin
from django.urls import path
from restaurant import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('menu/', views.menu, name='menu'),
    path('order/', views.order, name='order'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('checkout/', views.checkout, name='checkout')
] 