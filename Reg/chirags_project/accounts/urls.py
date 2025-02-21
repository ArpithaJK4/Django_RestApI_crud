from django.urls import path

from . import views
from .views import register, user_login, user_logout, user_home, get_user_by_id, get_all_users, update_profile, \
    profile_view

urlpatterns = [
    path('', user_home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile_view, name='profile'),
    # API Endpoints
    path('api/users/<int:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('api/users/', get_all_users, name='get_all_users'),
    path("update-profile/", update_profile, name="update_profile"),
    ]