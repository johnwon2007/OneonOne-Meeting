from .views import login_view, register_view, logout_view, profile_details, profile_edit_view, profile_contact_create_view, profile_contacts_view, profile_contact_edit_view
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'
urlpatterns = [
    path('login/', login_view.LoginView.as_view() , name='login'),
    path('register/', register_view.RegisterView.as_view() , name='register'),
    path('logout/', logout_view.LogoutView.as_view() , name='logout'),
    path('profile/details/', profile_details.ProfileDetailsView.as_view() , name='profile_details'),
    path('profile/edit/', profile_edit_view.ProfileEditView.as_view() , name='edit'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/contacts/all/', profile_contacts_view.ContactListView.as_view() , name='contacts'),
    path('profile/contacts/create/', profile_contact_create_view.ContactCreateView.as_view() , name='create_contact'),
    path('profile/contacts/edit/<int:pk>/', profile_contact_edit_view.ContactUpdateDeleteView.as_view() , name='edit_contact'),
    
]