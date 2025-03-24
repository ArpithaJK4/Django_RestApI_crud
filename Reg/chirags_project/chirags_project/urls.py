from django.contrib import admin
from django.urls import path, include
import accounts.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('accounts.urls')),  # Add this
    path('', views.user_home, name='home'),
]
