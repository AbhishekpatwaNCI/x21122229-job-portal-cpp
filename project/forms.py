from django import forms

from .models import *


class JobForm(forms.ModelForm):
    class Meta:
        model = new_job
        fields = [
            "job_title",
            "job_description",
            "job_location",
            "job_salary",
            "job_company",
            "job_contact",
            "job_email",
            "job_image",
        ]

class CandidateProfile(forms.ModelForm):
    class Meta:
        model = candidate
        fields = [
            "candidate_email",
            "candidate_phone",
            "candidate_location",
            "candidate_experience",
            "candidate_resume",
        ]
