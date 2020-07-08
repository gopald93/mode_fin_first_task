from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

#comapny model extending the user model
class Company(models.Model):
    company_name = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name=models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.brand_name
# company_agent models to store the agent data and have ForeignKey key relationaship with Company
class company_agent(models.Model):
    company=models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    company_agent_name=models.CharField(max_length=100,null=True,blank=True)
    no_of_call_attended=models.IntegerField(default=0)
    total_time_spent_for_call_attended=models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
       return self.company_agent_name
#not useful ...just for expriments
class Admin_Log_Activity(models.Model):
    company_admin_name=models.ForeignKey(company_agent, null=True, blank=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    log_in_time=models.DateTimeField(null=True,blank=True)
    log_out_time=models.DateTimeField(null=True,blank=True)
    details_of_activity = models.TextField(null=True,blank=True)

    def __str__(self):
       return self.company_admin_name.company_agent_name
# Main_Log_Activity model to maintain admin activity log and have no ForeignKey relationship
class Main_Log_Activity(models.Model):
    user=models.CharField(max_length=100,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    log_in_time=models.DateTimeField(null=True,blank=True)
    log_out_time=models.DateTimeField(null=True,blank=True)
    details_of_activity = models.TextField(null=True,blank=True)

    def __str__(self):
       return self.user

#when comapny angent will be craete by admin then created log will be maintain in activity log using this
def log_activity_add_agent(sender,instance,**kwargs):
    log_messages="%s is created by %s"%(instance.company_agent_name,instance.company.company_name.username)
    Main_Log_Activity.objects.create(user=instance.company.company_name.username,details_of_activity=log_messages)

#when comapny angent will be deleted by admin then created log will be maintain in activity log using this
def log_activity_delete_agent(sender,instance,**kwargs):
    log_messages="%s is deleted by %s"%(instance.company_agent_name,instance.company.company_name.username)
    Main_Log_Activity.objects.create(user=instance.company.company_name.username,details_of_activity=log_messages)
 
post_save.connect(log_activity_add_agent,sender=company_agent) 
post_delete.connect(log_activity_delete_agent,sender=company_agent)   


##creditionals
# ###############google########################
# username:
# pichai_sundararajan
# passwprd:
# pichai
# email
# google@gmail.com
###################

# ###############Amazon########################
# username:
# jeff_bezos
# passwprd:
# jeff
# email
# amazon@gmail.com
# ###############flipkart########################
# username:
# kalyan_krishnamurthy
# passwprd:
# kalyan
# email
# flipkart@gmail.com




