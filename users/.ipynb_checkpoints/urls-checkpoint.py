from django.urls import path
from . import views
from django.contrib.auth.views import LoginView




urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register')
]

