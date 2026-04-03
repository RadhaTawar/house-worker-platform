import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house_worker_platform.settings')
django.setup()

from authentication.models import User, WorkerProfile, EmployerProfile
from hiring.models import Job, JobCategory, JobApplication
from django.utils import timezone

def create_sample_data():
    print("Creating sample data...")
    
    # Create job categories
    categories = [
        ("Cleaning", "Professional cleaning services for homes and offices"),
        ("Cooking", "Home cooking and meal preparation services"),
        ("Childcare", "Babysitting and childcare services"),
        ("Gardening", "Lawn care and gardening services"),
        ("Elderly Care", "Care and support for elderly individuals"),
        ("Pet Care", "Pet sitting and walking services"),
        ("Maintenance", "Home maintenance and repair services"),
        ("Laundry", "Washing, ironing, and laundry services"),
    ]
    
    for name, description in categories:
        category, created = JobCategory.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        if created:
            print(f"Created category: {name}")
    
    # Create sample workers
    workers_data = [
        {
            'username': 'john_worker',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'age': 28,
            'gender': 'male',
            'experience_years': 5,
            'skills': 'cleaning, cooking, gardening',
            'hourly_rate': 15.00,
            'bio': 'Experienced house worker with 5 years of experience. Specialized in cleaning and basic cooking.'
        },
        {
            'username': 'mary_worker',
            'email': 'mary@example.com',
            'first_name': 'Mary',
            'last_name': 'Johnson',
            'age': 32,
            'gender': 'female',
            'experience_years': 8,
            'skills': 'childcare, cooking, elderly care',
            'hourly_rate': 18.00,
            'bio': 'Professional childcare provider with 8 years of experience. Also skilled in cooking and elderly care.'
        },
        {
            'username': 'robert_worker',
            'email': 'robert@example.com',
            'first_name': 'Robert',
            'last_name': 'Brown',
            'age': 35,
            'gender': 'male',
            'experience_years': 10,
            'skills': 'maintenance, gardening, pet care',
            'hourly_rate': 20.00,
            'bio': 'Handyman with 10 years of experience in home maintenance and repairs.'
        },
        {
            'username': 'sarah_worker',
            'email': 'sarah@example.com',
            'first_name': 'Sarah',
            'last_name': 'Davis',
            'age': 26,
            'gender': 'female',
            'experience_years': 3,
            'skills': 'laundry, cleaning, pet care',
            'hourly_rate': 12.00,
            'bio': 'Young and energetic worker specializing in laundry services and pet care.'
        },
    ]
    
    for worker_data in workers_data:
        user, created = User.objects.get_or_create(
            username=worker_data['username'],
            defaults={
                'email': worker_data['email'],
                'first_name': worker_data['first_name'],
                'last_name': worker_data['last_name'],
                'role': 'worker',
                'is_active': True,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created worker user: {user.username}")
            
            # Create worker profile
            profile = WorkerProfile.objects.create(
                user=user,
                age=worker_data['age'],
                gender=worker_data['gender'],
                experience_years=worker_data['experience_years'],
                skills=worker_data['skills'],
                hourly_rate=worker_data['hourly_rate'],
                bio=worker_data['bio'],
                is_verified=True,
                rating=4.5,
                total_jobs=20,
            )
            print(f"Created worker profile for: {user.username}")
    
    # Create sample employers
    employers_data = [
        {
            'username': 'alice_employer',
            'email': 'alice@example.com',
            'first_name': 'Alice',
            'last_name': 'Wilson',
            'company_name': 'Wilson Family',
            'company_type': 'Private Household',
            'contact_person': 'Alice Wilson',
        },
        {
            'username': 'bob_employer',
            'email': 'bob@example.com',
            'first_name': 'Bob',
            'last_name': 'Taylor',
            'company_name': 'Taylor Properties',
            'company_type': 'Property Management',
            'contact_person': 'Bob Taylor',
        },
    ]
    
    for employer_data in employers_data:
        user, created = User.objects.get_or_create(
            username=employer_data['username'],
            defaults={
                'email': employer_data['email'],
                'first_name': employer_data['first_name'],
                'last_name': employer_data['last_name'],
                'role': 'employer',
                'is_active': True,
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created employer user: {user.username}")
            
            # Create employer profile
            profile = EmployerProfile.objects.create(
                user=user,
                company_name=employer_data['company_name'],
                company_type=employer_data['company_type'],
                contact_person=employer_data['contact_person'],
                description=f'Looking for reliable house workers for {employer_data["company_name"]}'
            )
            print(f"Created employer profile for: {user.username}")
    
    # Create sample jobs
    employers = User.objects.filter(role='employer')
    categories = JobCategory.objects.all()
    
    jobs_data = [
        {
            'title': 'House Cleaning Service',
            'description': 'Need a reliable house cleaner for weekly cleaning of 3-bedroom house. Duties include vacuuming, mopping, bathroom cleaning, and kitchen cleaning.',
            'category': categories[0],  # Cleaning
            'employer': employers[0],
            'location': 'New York, NY',
            'salary_range': '$15-$20/hour',
            'is_urgent': False,
            'requirements': 'Experience in house cleaning preferred. Must be trustworthy and punctual.',
        },
        {
            'title': 'Childcare Provider Needed',
            'description': 'Looking for an experienced childcare provider for 2 children (ages 3 and 6). Part-time position, Monday to Friday, 9 AM to 2 PM.',
            'category': categories[2],  # Childcare
            'employer': employers[0],
            'location': 'Los Angeles, CA',
            'salary_range': '$18-$22/hour',
            'is_urgent': True,
            'requirements': 'Must have experience with childcare. References required.',
        },
        {
            'title': 'Garden Maintenance',
            'description': 'Need someone for regular garden maintenance including lawn mowing, hedge trimming, and general garden upkeep.',
            'category': categories[3],  # Gardening
            'employer': employers[1],
            'location': 'Chicago, IL',
            'salary_range': '$20-$25/hour',
            'is_urgent': False,
            'requirements': 'Experience with garden tools and maintenance. Physical fitness required.',
        },
        {
            'title': 'Home Cooking Services',
            'description': 'Seeking a cook to prepare meals for a family of 4. Need help with daily dinner preparation and some meal prep.',
            'category': categories[1],  # Cooking
            'employer': employers[1],
            'location': 'Houston, TX',
            'salary_range': '$16-$20/hour',
            'is_urgent': False,
            'requirements': 'Experience in cooking various cuisines. Food safety knowledge required.',
        },
    ]
    
    for job_data in jobs_data:
        job, created = Job.objects.get_or_create(
            title=job_data['title'],
            defaults={
                'description': job_data['description'],
                'category': job_data['category'],
                'employer': job_data['employer'],
                'location': job_data['location'],
                'salary_range': job_data['salary_range'],
                'is_urgent': job_data['is_urgent'],
                'requirements': job_data['requirements'],
                'status': 'open',
            }
        )
        if created:
            print(f"Created job: {job.title}")
    
    # Create sample job applications
    workers = User.objects.filter(role='worker')
    jobs = Job.objects.all()
    
    applications_data = [
        {
            'job': jobs[0],  # House Cleaning
            'worker': workers[0],  # John Worker
            'cover_letter': 'I have 5 years of experience in house cleaning and can provide excellent references. I am reliable and detail-oriented.',
            'proposed_rate': 16.00,
        },
        {
            'job': jobs[1],  # Childcare
            'worker': workers[1],  # Mary Worker
            'cover_letter': 'I have 8 years of experience in childcare and love working with children. I am certified in first aid and CPR.',
            'proposed_rate': 19.00,
        },
        {
            'job': jobs[2],  # Garden Maintenance
            'worker': workers[2],  # Robert Worker
            'cover_letter': 'I have 10 years of experience in garden maintenance and have all necessary tools. I am physically fit and reliable.',
            'proposed_rate': 22.00,
        },
        {
            'job': jobs[3],  # Home Cooking
            'worker': workers[3],  # Sarah Worker
            'cover_letter': 'I specialize in home cooking and can prepare a variety of cuisines. I am knowledgeable about food safety.',
            'proposed_rate': 17.00,
        },
    ]
    
    for app_data in applications_data:
        application, created = JobApplication.objects.get_or_create(
            job=app_data['job'],
            worker=app_data['worker'],
            defaults={
                'cover_letter': app_data['cover_letter'],
                'proposed_rate': app_data['proposed_rate'],
                'status': 'pending',
            }
        )
        if created:
            print(f"Created application for job: {application.job.title} by {application.worker.username}")
    
    print("\nSample data creation completed!")
    print("\nLogin credentials:")
    print("Admin: username=admin, password=[set during createsuperuser]")
    print("Workers: username=john_worker/mary_worker/robert_worker/sarah_worker, password=password123")
    print("Employers: username=alice_employer/bob_employer, password=password123")

if __name__ == '__main__':
    create_sample_data()
