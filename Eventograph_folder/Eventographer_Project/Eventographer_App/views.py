from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Customer
from .serializers import CustomerSerializer, LoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer



from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            token = customer.generate_token()
            return Response({"message": "Registration successful", "token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['customer_email']
            password = serializer.validated_data['password']

            try:
                customer = Customer.objects.get(customer_email=email.lower())  # Normalize email
            except Customer.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

            if check_password(password, customer.password):
                token = customer.generate_token()
                customer.last_logged_in = now()
                customer.save()
                return Response({"message": "Login successful", "token": token}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Customer  # Ensure your Customer model is imported
from .serializers import CustomerSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id=None):
        """
        Fetch profile details of a user by ID.
        If no ID is provided, fetch the authenticated user's profile.
        """
        if user_id:
            user = get_object_or_404(Customer, id=user_id)  # Fetch user by ID
        else:
            user = request.user  # Fetch logged-in user

        serializer = CustomerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditProfileView(APIView):
    authentication_classes = []
    permission_classes = []

    def put(self, request):
        customer = request.user
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = Customer.objects.get(customer_email=serializer.validated_data['customer_email'])
                return Response({"message": "Reset link sent to email"}, status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request, customer_id):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = Customer.objects.get(pk=customer_id)
                customer.password = make_password(serializer.validated_data['new_password'])
                customer.save()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
