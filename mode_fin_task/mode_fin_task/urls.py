from django.contrib import admin
from django.urls import path,include
from company.views import user_login, user_logout,recovery_creditional

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', include('company.urls')),
    path('login/', user_login, name="user_login"),
    path('logout/', user_logout, name="user_logout"),
    path('recovery_creditional/', recovery_creditional, name="recovery_creditional"),

]
