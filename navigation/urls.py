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
from django.contrib import admin
from django.urls import path
from .views import Object_list, login_user, logout_user, register_user, Reset_password, User_list, Distance_sum_update, Route_created_count_update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('objects/', Object_list.as_view(), name='object_list'),
    path('auth/login', login_user, name='login'),
    path('auth/logout', logout_user, name='logout'),
    path('auth/register', register_user, name='register'),
    #path('auth/reset-password-request', views.ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path('auth/reset-password', Reset_password.as_view(), name='reset_password'),
    path('all_users/', User_list.as_view(), name='user_list'),
    path('user-distance-sum', Distance_sum_update.as_view(), name='distance_sum_update'),
    path('user-route-created-count', Route_created_count_update.as_view(), name='route_created_count_update')
]
