from django.urls import path
from .views import RegisterView, LoginView, CustomerProfileView, CustomerListView, CustomerUpdateView, user_logout




urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/<int:customer_id>/', CustomerProfileView.as_view(), name='customer-profile'),
    path('profiles/', CustomerListView.as_view(), name='customer-list'),
    path('profile/update/<int:customer_id>/', CustomerUpdateView.as_view(), name='customer-update'),
    path("logout/", user_logout, name="logout"),

]



