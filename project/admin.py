from django.contrib import admin

from .models import *



admin.site.register(employee)


@admin.register(new_job)
class new_jobAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "job_description",
        "job_location",
        "job_salary",
        "job_company",
        "job_contact",
        "job_email",
        "employee_id",
        "created_at",
        "updated_at",
    )


@admin.register(candidate)
class candidateAdmin(admin.ModelAdmin):
    list_display = (
        "candidate_id",
        "candidate_name",
        "candidate_email",
        "candidate_phone",
        "candidate_location",
        "candidate_experience",
        "candidate_resume",
        "created_at",
        "updated_at",
    )

admin.site.register(applied_job)    
