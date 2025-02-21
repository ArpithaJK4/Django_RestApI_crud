
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.utils.timezone import now
from .forms import CustomUserCreationForm, UserUpdateForm

from rest_framework.authtoken.models import Token

from rest_framework.generics import get_object_or_404



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.login_time = now()  # Set login time at registration
            user.save()

            login(request, user)
            return JsonResponse({'message': 'User registered successfully'})
        else:
            print("Form errors:", form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(f"Email: {email}, Password: {password}")

        # Authenticate user using email
        user = authenticate(request, username=email, password=password)
        print(f"Authenticated User: {user}")

        if user is not None:
            user.login_time = now()  # Update login time

            # Generate new token
            token, _ = Token.objects.get_or_create(user=user)
            print(f"New Token: {token.key}")

            # Store token in User model using update()
            User.objects.filter(id=user.id).update(token=token.key, login_time=user.login_time)

            login(request, user)
            return JsonResponse({'message': 'Login successful', 'token': token.key})
        else:
            print("Invalid credentials")
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return render(request, 'users/login.html')

def user_logout(request):
    user = request.user
    if user.is_authenticated:
        Token.objects.filter(user=user).delete()  # Remove token from DB on logout
        User.objects.filter(email=user.email).update(token=None)  # Clear token from user model
        logout(request)

    return redirect('home')

def get_all_users(request):
    users = User.objects.all()  # Fetch all users as objects
    return render(request, 'users/all_users.html', {'users': users})

def get_user_by_id(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Ensure the user is fetched correctly
    return render(request, 'users/user_detail.html', {'user': user})

def user_home(request):
    return render(request, 'users/home.html')

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CustomUser

User = get_user_model()
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
 # Ensure your User model is correctly imported

@login_required
def update_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "users/profile.html", {"form": form})


from django.shortcuts import render

def profile_view(request):
    return render(request, 'profile.html')  # ✅ Ensure 'profile.html' exists in templates
