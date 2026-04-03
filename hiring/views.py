from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from .models import Job, JobCategory, JobApplication, Review
from authentication.models import User, EmployerProfile
from .forms import JobPostForm, ReviewForm

@login_required
def employer_dashboard(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied. Employer role required.')
        return redirect('authentication:home')
    
    try:
        profile = request.user.employer_profile
    except EmployerProfile.DoesNotExist:
        return redirect('authentication:complete_employer_profile')
    
    # Get employer's jobs
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    
    # Get job statistics
    total_jobs = jobs.count()
    open_jobs = jobs.filter(status='open').count()
    in_progress_jobs = jobs.filter(status='in_progress').count()
    completed_jobs = jobs.filter(status='completed').count()
    
    # Get recent applications
    recent_applications = JobApplication.objects.filter(
        job__employer=request.user
    ).order_by('-applied_at')[:5]
    
    context = {
        'profile': profile,
        'jobs': jobs,
        'total_jobs': total_jobs,
        'open_jobs': open_jobs,
        'in_progress_jobs': in_progress_jobs,
        'completed_jobs': completed_jobs,
        'recent_applications': recent_applications,
    }
    
    return render(request, 'hiring/employer_dashboard.html', context)

@login_required
def post_job(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied. Employer role required.')
        return redirect('authentication:home')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('hiring:employer_dashboard')
    else:
        form = JobPostForm()
    
    return render(request, 'hiring/post_job.html', {'form': form})

@login_required
def my_jobs(request):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied. Employer role required.')
        return redirect('authentication:home')
    
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        jobs = jobs.filter(status=status_filter)
    
    context = {
        'jobs': jobs,
        'status_filter': status_filter,
    }
    
    return render(request, 'hiring/my_jobs.html', context)

@login_required
def manage_applications(request, job_id):
    if request.user.role != 'employer':
        messages.error(request, 'Access denied. Employer role required.')
        return redirect('authentication:home')
    
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.applications.all().order_by('-applied_at')
    
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        action = request.POST.get('action')
        
        application = get_object_or_404(JobApplication, id=application_id, job=job)
        
        if action == 'accept':
            application.status = 'accepted'
            job.status = 'in_progress'
            job.save()
            messages.success(request, f'Application from {application.worker.username} accepted!')
        elif action == 'reject':
            application.status = 'rejected'
            messages.info(request, f'Application from {application.worker.username} rejected.')
        
        application.save()
        return redirect('hiring:manage_applications', job_id=job_id)
    
    return render(request, 'hiring/manage_applications.html', {
        'job': job,
        'applications': applications,
    })

class JobListView(ListView):
    model = Job
    template_name = 'hiring/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Job.objects.filter(status='open').order_by('-created_at')
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        # Filter by category
        category_filter = self.request.GET.get('category', '')
        if category_filter:
            queryset = queryset.filter(category_id=category_filter)
        
        # Filter by location
        location_filter = self.request.GET.get('location', '')
        if location_filter:
            queryset = queryset.filter(location__icontains=location_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['location_filter'] = self.request.GET.get('location', '')
        context['categories'] = JobCategory.objects.all()
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'hiring/job_detail.html'
    context_object_name = 'job'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        
        # Get applications for this job (only if user is the employer)
        if self.request.user.is_authenticated and self.request.user == job.employer:
            context['applications'] = job.applications.all().order_by('-applied_at')
        
        # Check if current worker has already applied
        if self.request.user.is_authenticated and self.request.user.role == 'worker':
            context['has_applied'] = JobApplication.objects.filter(
                job=job, worker=self.request.user
            ).exists()
        
        return context

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin role required.')
        return redirect('home')
    
    # Get statistics
    total_users = User.objects.count()
    total_workers = User.objects.filter(role='worker').count()
    total_employers = User.objects.filter(role='employer').count()
    total_jobs = Job.objects.count()
    open_jobs = Job.objects.filter(status='open').count()
    
    # Get recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Get recent jobs
    recent_jobs = Job.objects.order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_workers': total_workers,
        'total_employers': total_employers,
        'total_jobs': total_jobs,
        'open_jobs': open_jobs,
        'recent_users': recent_users,
        'recent_jobs': recent_jobs,
    }
    
    return render(request, 'admin/dashboard.html', context)
