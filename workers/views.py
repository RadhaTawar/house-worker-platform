from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from authentication.models import User, WorkerProfile
from hiring.models import Job, JobApplication

@login_required
def worker_dashboard(request):
    if request.user.role != 'worker':
        messages.error(request, 'Access denied. Worker role required.')
        return redirect('authentication:home')
    
    try:
        profile = request.user.worker_profile
    except WorkerProfile.DoesNotExist:
        return redirect('authentication:complete_worker_profile')
    
    # Get worker's applications
    applications = JobApplication.objects.filter(worker=request.user).order_by('-applied_at')
    
    # Get available jobs
    available_jobs = Job.objects.filter(status='open').order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'applications': applications,
        'available_jobs': available_jobs,
        'total_applications': applications.count(),
        'pending_applications': applications.filter(status='pending').count(),
        'accepted_applications': applications.filter(status='accepted').count(),
    }
    
    return render(request, 'workers/dashboard.html', context)

@login_required
def worker_profile(request):
    if request.user.role != 'worker':
        messages.error(request, 'Access denied. Worker role required.')
        return redirect('authentication:home')
    
    try:
        profile = request.user.worker_profile
    except WorkerProfile.DoesNotExist:
        return redirect('authentication:complete_worker_profile')
    
    return render(request, 'workers/profile.html', {'profile': profile})

class WorkerListView(ListView):
    model = WorkerProfile
    template_name = 'workers/worker_list.html'
    context_object_name = 'workers'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = WorkerProfile.objects.filter(is_verified=True, availability=True)
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(user__username__icontains=search_query) |
                Q(skills__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query)
            )
        
        # Filter by skills
        skill_filter = self.request.GET.get('skill', '')
        if skill_filter:
            queryset = queryset.filter(skills__icontains=skill_filter)
        
        # Sort by
        sort_by = self.request.GET.get('sort', 'rating')
        if sort_by == 'rating':
            queryset = queryset.order_by('-rating')
        elif sort_by == 'experience':
            queryset = queryset.order_by('-experience_years')
        elif sort_by == 'rate_low':
            queryset = queryset.order_by('hourly_rate')
        elif sort_by == 'rate_high':
            queryset = queryset.order_by('-hourly_rate')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['skill_filter'] = self.request.GET.get('skill', '')
        context['sort_by'] = self.request.GET.get('sort', 'rating')
        return context

class WorkerDetailView(DetailView):
    model = WorkerProfile
    template_name = 'workers/worker_detail.html'
    context_object_name = 'worker'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        
        # Get worker's reviews
        from hiring.models import Review
        reviews = Review.objects.filter(worker=worker.user).order_by('-created_at')
        
        # Get worker's completed jobs
        completed_jobs = JobApplication.objects.filter(
            worker=worker.user, 
            status='accepted',
            job__status='completed'
        )
        
        context['reviews'] = reviews
        context['completed_jobs'] = completed_jobs.count()
        return context

@login_required
def browse_jobs(request):
    if request.user.role != 'worker':
        messages.error(request, 'Access denied. Worker role required.')
        return redirect('authentication:home')
    
    jobs = Job.objects.filter(status='open').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        jobs = jobs.filter(category_id=category_filter)
    
    from hiring.models import JobCategory
    categories = JobCategory.objects.all()
    
    # Mark selected category
    for cat in categories:
        cat.is_selected = str(cat.id) == category_filter

    context = {
        'jobs': jobs,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    
    return render(request, 'workers/browse_jobs.html', context)

@login_required
def apply_job(request, job_id):
    if request.user.role != 'worker':
        messages.error(request, 'Access denied. Worker role required.')
        return redirect('authentication:home')
    
    job = get_object_or_404(Job, id=job_id)
    
    # Check if already applied
    if JobApplication.objects.filter(job=job, worker=request.user).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('workers:browse_jobs')
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        proposed_rate = request.POST.get('proposed_rate')
        
        if cover_letter:
            application = JobApplication.objects.create(
                job=job,
                worker=request.user,
                cover_letter=cover_letter,
                proposed_rate=proposed_rate if proposed_rate else None
            )
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('workers:worker_dashboard')
        else:
            messages.error(request, 'Please provide a cover letter.')
    
    return render(request, 'workers/apply_job.html', {'job': job})
