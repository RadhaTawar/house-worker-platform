from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, WorkerProfile, EmployerProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'address')}),
        ('Profile', {'fields': ('role', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

@admin.register(WorkerProfile)
class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'experience_years', 'hourly_rate', 'is_verified', 'rating', 'availability')
    list_filter = ('gender', 'is_verified', 'availability', 'created_at')
    search_fields = ('user__username', 'skills')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'age', 'gender', 'experience_years')}),
        ('Professional Info', {'fields': ('skills', 'hourly_rate', 'availability', 'bio')}),
        ('Verification', {'fields': ('id_proof', 'is_verified')}),
        ('Stats', {'fields': ('rating', 'total_jobs')}),
    )

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_type', 'contact_person', 'created_at')
    list_filter = ('company_type', 'created_at')
    search_fields = ('user__username', 'company_name', 'contact_person')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Company Info', {'fields': ('company_name', 'company_type', 'contact_person')}),
        ('Contact Info', {'fields': ('website',)}),
        ('Description', {'fields': ('description',)}),
    )
