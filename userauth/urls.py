# urls.py
from django.urls import path
from .views import UserRegistrationView, UserLoginView, OrganisationListView, CreatedOrganisationsView

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('api/created-organisations/', CreatedOrganisationsView.as_view(), name='created-organisations'),
]