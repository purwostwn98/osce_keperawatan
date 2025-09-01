from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('cas-callback/', views.cas_callback, name='cas_callback'),
]
