from django.urls import path
from . import views

app_name = 'workers'

urlpatterns = [
    path('dashboard/', views.worker_dashboard, name='worker_dashboard'),
    path('profile/', views.worker_profile, name='worker_profile'),
    path('list/', views.WorkerListView.as_view(), name='worker_list'),
    path('detail/<int:pk>/', views.WorkerDetailView.as_view(), name='worker_detail'),
    path('browse-jobs/', views.browse_jobs, name='browse_jobs'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
]
