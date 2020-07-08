from django.urls import path
from company.views import *

urlpatterns = [
    path('', company_wise_list, name='company_wise_list'),
    path('activity_log/', activity_log, name='activity_log'),]