from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('complete-worker-profile/', views.complete_worker_profile, name='complete_worker_profile'),
    path('complete-employer-profile/', views.complete_employer_profile, name='complete_employer_profile'),
    path('home/', views.home_view, name='home'),
]
