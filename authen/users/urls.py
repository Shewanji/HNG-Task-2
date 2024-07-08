from django.urls import path
from .views import RegisterView, LoginView, UserView, OrganisationView, SingleOrganisationView, AddUserToOrganisationView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/<uuid:pk>', UserView.as_view(), name='user_detail'),
    path('api/organisations', OrganisationView.as_view(), name='organisations'),
    path('api/organisations/<uuid:orgId>', SingleOrganisationView.as_view(), name='organisation_detail'),
    path('api/organisations/<uuid:orgId>/users', AddUserToOrganisationView.as_view(), name='add_user_to_organisation'),
]

