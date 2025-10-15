from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm
from accounts.models import User
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden  # Added HttpResponse



def home(request):
    return render(request, 'home.html')

def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    if request.user.is_authenticated and request.user.user_type == 'job_seeker':
        has_applied = JobApplication.objects.filter(job=job, applicant=request.user).exists()
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied
    })

@login_required
def job_create(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    
    return render(request, 'jobs/job_form.html', {'form': form, 'title': 'Post New Job'})

@login_required
def job_apply(request, pk):
    if request.user.user_type != 'job_seeker':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('home')
    
    job = get_object_or_404(Job, pk=pk)
    
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = JobApplicationForm()
    
    return render(request, 'jobs/job_apply.html', {'form': form, 'job': job})

@login_required
def employer_dashboard(request):
    if request.user.user_type != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    applications = JobApplication.objects.filter(job__employer=request.user).order_by('-applied_at')
    
    return render(request, 'dashboard/employer_dashboard.html', {
        'jobs': jobs,
        'applications': applications
    })

@login_required
def my_applications(request):
    if request.user.user_type != 'job_seeker':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    applications = JobApplication.objects.filter(applicant=request.user).order_by('-applied_at')
    return render(request, 'dashboard/my_applications.html', {'applications': applications})

@login_required
def profile(request):
    return render(request, 'profile.html')

# Add registration view here for frontend
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        phone_number = request.POST.get('phone_number')
        company_name = request.POST.get('company_name')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        
        if password != password2:
            messages.error(request, "Passwords don't match.")
            return render(request, 'registration/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'registration/register.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                phone_number=phone_number,
                company_name=company_name if user_type == 'employer' else '',
                skills=skills if user_type == 'job_seeker' else '',
                experience=experience if user_type == 'job_seeker' else ''
            )
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'registration/register.html')
    
    return render(request, 'registration/register.html')






# ... (keep existing views and add these new ones)

@login_required
def application_detail(request, pk):
    """View application details - accessible by both employer and applicant"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    # Check if user has permission to view this application
    if request.user != application.applicant and request.user != application.job.employer:
        return HttpResponseForbidden("You don't have permission to view this application.")
    
    context = {
        'application': application,
        'can_manage': request.user == application.job.employer,  # Employer can manage status
        'is_applicant': request.user == application.applicant,
    }
    return render(request, 'jobs/application_detail.html', context)

@login_required
def update_application_status(request, pk):
    """Employer can update application status"""
    if request.method == 'POST' and request.user.user_type == 'employer':
        application = get_object_or_404(JobApplication, pk=pk, job__employer=request.user)
        new_status = request.POST.get('status')
        notes = request.POST.get('employer_notes', '')
        
        if new_status in dict(JobApplication.APPLICATION_STATUS):
            application.status = new_status
            application.employer_notes = notes
            application.save()
            
            messages.success(request, f'Application status updated to {application.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('application_detail', pk=pk)

@login_required
def employer_application_list(request, job_id=None):
    """Employer view of all applications, optionally filtered by job"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    applications = JobApplication.objects.filter(job__employer=request.user)
    
    if job_id:
        job = get_object_or_404(Job, pk=job_id, employer=request.user)
        applications = applications.filter(job=job)
        context = {'applications': applications.order_by('-applied_at'), 'current_job': job}
    else:
        context = {'applications': applications.order_by('-applied_at')}
    
    return render(request, 'dashboard/employer_applications.html', context)


    
@login_required
def download_resume(request, pk):
    """Download resume file"""
    application = get_object_or_404(JobApplication, pk=pk)
    
    # Check permissions
    if request.user != application.applicant and request.user != application.job.employer:
        return HttpResponseForbidden("You don't have permission to download this resume.")
    
    if application.resume:
        try:
            response = HttpResponse(application.resume.read(), content_type='application/octet-stream')
            filename = f"{application.applicant.username}_resume.pdf"
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        except Exception as e:
            messages.error(request, f'Error downloading resume: {str(e)}')
            return redirect('application_detail', pk=pk)
    else:
        messages.error(request, 'Resume not found.')
        return redirect('application_detail', pk=pk)