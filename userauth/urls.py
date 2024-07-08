# urls.py
from django.urls import path
from .views import UserRegistrationView, UserLoginView, OrganisationListView, CreatedOrganisationsView, UserDetailView, UserOrganisationsView

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', UserLoginView.as_view(), name='login'),
    path('api/organisations/', OrganisationListView.as_view(), name='organisations'),
    path('api/created-organisations/', CreatedOrganisationsView.as_view(), name='created-organisations'),
    path('api/users/<int:id>/', UserDetailView.as_view(), name='user_detail'),
    path('api/organisations', UserOrganisationsView.as_view(), name='user_organisations'),
]