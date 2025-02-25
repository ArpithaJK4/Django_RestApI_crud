from django.urls import path
from .views import RegisterView, LoginView, ProfileView, EditProfileView, ForgotPasswordView, ResetPasswordView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),  # Fetch current user
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile_by_id'),
    path('edit-profile/<int:customer_id>/', EditProfileView.as_view(), name='edit-profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<int:customer_id>/', ResetPasswordView.as_view(), name='reset-password'),
    path('logout/', LogoutView.as_view(), name='logout'),


]


