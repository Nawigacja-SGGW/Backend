"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import Distance_sum_update, Login, Logout, Object_list, Object_single, Register, Reset_password, Reset_password_request, Route_created_count_update, User_list
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin', admin.site.urls),
    path('all-users', User_list.as_view(), name='user_list'),
    path('auth/login', Login.as_view(), name='login'),
    path('auth/logout', Logout.as_view(), name='logout'),
    path('auth/register', Register.as_view(), name='register'),
    path('auth/reset-password', Reset_password.as_view(), name='reset_password'),
    path('auth/reset-password-request', Reset_password_request.as_view(), name='reset_password_request'),
    path('objects', Object_list.as_view(), name='object_list'),
    path('single-object', Object_single.as_view(), name='object_single'),
    path('user-distance-sum', Distance_sum_update.as_view(), name='distance_sum_update'),
    path('user-route-created-count', Route_created_count_update.as_view(), name='route_created_count_update')
]