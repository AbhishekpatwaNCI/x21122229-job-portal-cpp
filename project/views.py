from email import message
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render , redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import login, authenticate ,logout as deauth
from django.contrib.auth.decorators import login_required

def index(request):
    user_type = ''
    if request.user.is_authenticated:
        
        if employee.objects.filter(user=request.user).exists():
            user_type = 'employee'
        elif candidate.objects.filter(candidate_id=request.user).exists(): 
            user_type = 'candidate' 
        else:
            user_type = 'none'    
        
    context = {
            'jobs':new_job.objects.all(),
            'type':user_type,
        }    

    return render(request, "index.html" , context)
    
def candidate_home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/') 
    if not candidate.objects.filter(candidate_id=request.user).exists():
        messages.success(request, 'You are not a candidate')
        return redirect('project:index')        

    cand = candidate.objects.filter(candidate_id=request.user).first()
    jobs= applied_job.objects.filter(candidate_id=cand)
    context={
        'cand':cand,
        'jobs':jobs,
    }
    return render(request , 'candidate/candidate.html' , context)    


def profile_update(request , pk):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if not candidate.objects.filter(candidate_id=request.user).exists():
        return redirect('project:index')    
    get_instance=candidate.objects.filter(candidate_id=request.user).first()
    if request.method == 'POST':
        form = CandidateProfile(request.POST , request.FILES , instance=get_instance)
        get_emp=employee.objects.filter(user=request.user).first()
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated Successfully')
            return redirect('project:candidate-home')
        else:
            messages.success(request, 'Profile not Updated')
            return redirect('project:candidate-home')
    else:
        
        form = CandidateProfile(instance=get_instance)
    context = {
        'form':form,
    }
    return render(request , 'candidate/profile_update.html' , context)


def candidate_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone   = request.POST.get('phone')
        email   = request.POST.get('email')
        pass1   = request.POST.get('pass1')
        pass2   = request.POST.get('pass2')
        if not  pass1 == pass2:
            messages.success(request, 'Password not match')
            return redirect('project:candidate-register')
        if pass1.isnumeric():
            messages.success(request, 'Password should not be numeric')
            return redirect('project:candidate-register')
        if pass1.isalpha():
            messages.success(request, 'Password should not be alphabetic')
            return redirect('project:candidate-register')
                    
        if not len(phone) == 10:
            messages.success(request, 'Phone number must be 10 digit')
            return redirect('project:candidate-register')

        if User.objects.filter(username=username).exists():
            messages.success(request, 'Username already exists')
            return redirect('project:candidate-register')

        get_user=User.objects.create(
            username=username,
        )    
        get_user.set_password(pass1)
        get_user.save()
        get_candidate=candidate.objects.create(
            candidate_name=username,
            candidate_phone=phone,
            candidate_email=email,
            candidate_id=get_user,
        )
        messages.success(request, 'Register Successfully')
        login(request , get_user)
        return redirect('project:index')
    context={}
    return render(request , 'register/cand_register.html' , context)

def employee_home(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if not employee.objects.filter(user=request.user).exists():
        return redirect('project:index')

    get_emp=employee.objects.filter(user=request.user).first()
    get_job=new_job.objects.filter(employee_id=get_emp)         
    
    context={
        'jobs':get_job,
    }
    return render(request , 'employee/employee.html' , context)    

def employee_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1   = request.POST.get('pass1')
        pass2   = request.POST.get('pass2')
        if not  pass1 == pass2:
            messages.success(request, 'Password not match')
            return redirect('project:employee-register')
        if pass1.isnumeric():
            messages.success(request, 'Password should not be numeric')
            return redirect('project:employee-register')
        if pass1.isalpha():
            messages.success(request, 'Password should not be alphabetic')
            return redirect('project:employee-register')

        get_user=User.objects.create(
            username=username,
        )    
        get_user.set_password(pass1)
        get_user.save()
        get_candidate=employee.objects.create(
            user=get_user,
        )
        messages.success(request, 'Register Successfully')
        login(request , get_user)
        return redirect('project:index')
    context={}
    return render(request , 'register/emp_register.html' , context)

def add_new_job(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if not employee.objects.filter(user=request.user).exists():
        return redirect('project:index')    
    
    if request.method == 'POST':
        form = JobForm(request.POST ,request.FILES )
        get_emp=employee.objects.filter(user=request.user).first()
        if form.is_valid():
            ht=form.save(commit=False)
            ht.employee_id = get_emp
            ht.save()
            messages.success(request, 'Job Added Successfully')
            return redirect('project:employee-home')
        else:
            messages.success(request, 'Job not Added')
            return redirect('project:employee-home')
    else:
        form = JobForm()
    context = {
        'form':form,
    }
    return render(request , 'employee/add_job.html' , context)
def job_update(request , pk):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if not employee.objects.filter(user=request.user).exists():
        return redirect('project:index')    
    
    get_job=get_object_or_404(new_job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST ,request.FILES , instance=get_job , )
        if form.is_valid():
            form.save()
            messages.success(request, 'Job Updated Successfully')
            return redirect('project:employee-home')
        else:
            messages.success(request, 'Job not Updated')
            return redirect('project:employee-home')
    else:
        form = JobForm(instance=get_job)
    context = {
        'form':form,
    }
    return render(request , 'employee/add_job.html' , context)


def apply_job(request ,pk):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if not candidate.objects.filter(candidate_id=request.user).exists():
        messages.success(request, 'You are not a candidate')
        return redirect('project:index')    
    
    get_job=get_object_or_404(new_job, pk=pk)

    get_candidate=get_object_or_404(candidate, candidate_id=request.user)

    if not get_candidate.candidate_resume:
        messages.success(request, 'Please Upload Resume first')
        return redirect('project:candidate-home')
    
    if applied_job.objects.filter(candidate_id=get_candidate, new_job_id=get_job).exists():
        messages.success(request, 'Already Applied')
        return redirect('project:employee-home')
    else:
        get_applied=applied_job.objects.create(
            candidate_id=get_candidate,
            new_job_id=get_job,
        )
        messages.success(request, 'Applied Successfully')
        return redirect('project:candidate-home')   

def see_deatils(request , pk):
    if not request.user.is_authenticated:
        return redirect('/accounts/login/')
    if not employee.objects.filter(user=request.user).exists():
        messages.success(request, 'You are not a employee')
        return redirect('project:index')      
    
    get_job=new_job.objects.filter(pk=pk).first()
    context={
        'job':get_job,
    }
    return render(request,'employee/see_details.html', context)    
    
from django.http import JsonResponse,HttpResponse
def get_file(request,pk):
    get_obj=candidate.objects.get(id=pk)
    get_path=get_obj.candidate_resume.url
    urlFile=get_path.strip("/")
  
    with open(urlFile, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel") # mimetype is replaced by content_type for django 1.7
        response['Content-Disposition'] = 'inline; filename=' + urlFile
        return response
    
