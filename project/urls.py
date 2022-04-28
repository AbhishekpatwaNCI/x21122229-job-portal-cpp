from django.urls import path

from . import views

app_name = "project"

urlpatterns = [
    path("", views.index, name="index"),
    path("candidate-home/"     , views.candidate_home , name="candidate-home" ),
    path("profile-update/<int:pk>/", views.profile_update , name="profile-update"),
    path("candidate-register/"    , views.candidate_register , name="candidate-register" ),
    path("employee-home/", views.employee_home , name="employee-home" ),
    path("employee-register/", views.employee_register , name="employee-register" ),
    path("add-job",views.add_new_job , name="add-job"),
    path("job-update/<str:pk>/",views.job_update , name="job-update"),
    path("apply-job/<str:pk>/",views.apply_job , name="apply-job"),
    path("see-deatils/<str:pk>/",views.see_deatils , name="see-deatils"),
    path("resume/<str:pk>/", views.get_file , name="resume" ),
  
]
