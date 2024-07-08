"""
URL configuration for authen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.urls import path
from users.views import RegisterView, LoginView, UserView, OrganisationView, SingleOrganisationView, AddUserToOrganisationView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/<uuid:pk>', UserView.as_view(), name='user_detail'),
    path('api/organisations', OrganisationView.as_view(), name='organisations'),
    path('api/organisations/<uuid:orgId>', SingleOrganisationView.as_view(), name='organisation_detail'),
    path('api/organisations/<uuid:orgId>/users', AddUserToOrganisationView.as_view(), name='add_user_to_organisation'),
   
]