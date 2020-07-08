from django.shortcuts import render
from company.models import *
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse_lazy

#login related method
def user_login(request):
    context={}
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user= authenticate(request,username=username,password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            log_messages="%s user is login"%(username)  
            Main_Log_Activity.objects.create(user=username,log_in_time=timezone.now(),details_of_activity=log_messages)    
            return HttpResponseRedirect(reverse('company_wise_list'))
        else:
            context["error"]="Please Provide the valid username and password!!"
            return render(request,"auth/login_two.html",context)     
    else:
        return render(request,"auth/login_two.html",context)
#log_out related method
def user_logout(request):
    if request.method=="POST":
        username=request.user
        log_messages="%s user is logout"%(username)  
        Main_Log_Activity.objects.create(user=username,log_out_time=timezone.now(),details_of_activity=log_messages)    
        logout(request)
        return HttpResponseRedirect(reverse("user_login"))
#recovery the creditional using the emaail id
def recovery_creditional(request):
    context = {}
    if request.method == 'POST':
        email=request.POST["email"]
        username=request.POST["username"]
        password=request.POST["password"]
        confirm_password=request.POST["confirm_password"]
        if password!=confirm_password:
            context["error"]="password and confirm is not same!!"
            return render(request,"auth/recovery_creditional.html",context)
        else: 
            try:
                user_obj=User.objects.get(email=email)
                user_obj.username=username
                user_obj.set_password(password)
                user_obj.save()
                return HttpResponseRedirect(reverse("user_login"))
            except Exception as e:
                context["error"]=str(e)
                return render(request,"auth/recovery_creditional.html",context)    
    else:
        return render(request, "auth/recovery_creditional.html", context)
#showing the employee data         
@login_required(login_url="/login/")
def company_wise_list(request):
    context = {}
    company_obj=Company.objects.get(company_name__username=request.user)
    context['company_obj'] = company_obj
    context['title'] = 'Agent'
    return render(request, 'company/comapny_wise_profile.html', context)    
#showing activity of admin
@login_required(login_url="/login/")
def activity_log(request):
    context={}
    main_log_activity_obj=Main_Log_Activity.objects.filter(user=request.user)
    context['main_log_activity_obj'] = main_log_activity_obj
    context['title'] = 'Details of admin activity'
    return render(request, 'company/admin_activity_log.html', context)
