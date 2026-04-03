from django.urls import path
from . import views

app_name = 'hiring'

urlpatterns = [
    path('post-job/', views.post_job, name='post_job'),
    path('job-list/', views.JobListView.as_view(), name='job_list'),
    path('job-detail/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('manage-applications/<int:job_id>/', views.manage_applications, name='manage_applications'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
