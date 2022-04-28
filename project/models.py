from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class new_job(models.Model):
    job_title       = models.CharField(max_length=100)
    job_description = models.TextField()
    job_location    = models.CharField(max_length=100)
    job_salary      = models.PositiveIntegerField()
    job_company     = models.CharField(max_length=100)
    job_contact     = models.CharField(max_length=100)
    job_image      = models.ImageField(upload_to='JOBimages', blank=True)
    job_email       = models.EmailField()
    employee_id     = models.ForeignKey(employee, on_delete=models.CASCADE , related_name='employee')
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.job_title
    
    class Meta:
        ordering = ['-created_at']
     
class candidate(models.Model):
    candidate_id         = models.ForeignKey(User, on_delete=models.CASCADE , related_name='candidate')
    candidate_name       = models.CharField(max_length=100)
    candidate_email      = models.EmailField( null=True, blank=True, )
    candidate_phone      = models.PositiveIntegerField( null=True, blank=True, )
    candidate_location   = models.CharField(max_length=100, null=True, blank=True, )
    candidate_experience = models.CharField(max_length=100 ,null=True, blank=True, )
    candidate_resume     = models.FileField(upload_to='resume/' ,null=True, blank=True, )
    created_at           = models.DateTimeField(auto_now_add=True)
    updated_at           = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.candidate_name
    
    class Meta:
        ordering = ['-created_at']

class applied_job(models.Model):
    new_job_id = models.ForeignKey(new_job, on_delete=models.CASCADE , related_name='new_job')
    candidate_id = models.ForeignKey(candidate, on_delete=models.CASCADE , related_name='candidate')
