from django.contrib.auth import logout, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import Customer
from .serializers import CustomerSerializer, LoginSerializer
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()

            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
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


class CustomerProfileView(RetrieveAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'customer_id'
    permission_classes = [AllowAny]


class CustomerListView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


class CustomerUpdateView(RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'customer_id'
    permission_classes = [AllowAny]

from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db import transaction
from .models import Customer

@api_view(["POST"])
@permission_classes([AllowAny])
def user_logout(request):
    try:
        email = request.data.get("email")
        if not email:
            return Response({"error": "Customer email is required."}, status=400)

        customer = Customer.objects.filter(customer_email=email).first()
        if not customer:
            return Response({"error": "Customer not found."}, status=404)

        # Debug: Print all tokens in the database
        all_tokens = Token.objects.all()
        print("All Tokens in DB:")
        for t in all_tokens:
            print(f"User ID: {t.user_id}, Token: {t.key}")

        with transaction.atomic():
            tokens_deleted, _ = Token.objects.filter(user=customer).delete()

        if tokens_deleted:
            print(f"{tokens_deleted} token(s) deleted successfully")
            return Response({"message": "Logout successful, token deleted"}, status=200)
        else:
            print("No token found for this user")
            return Response({"error": "No active token found for user"}, status=404)

    except Exception as e:
        print(f"Error: {str(e)}")  # Debugging
        return Response({"error": str(e)}, status=400)



'''

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    user = request.user

    if user.is_authenticated:
        Token.objects.filter(user=user).delete()  # Delete authentication token
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

    return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class user_logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)



'''''

'''

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password reset link sent!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        # Reset password
        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"error": "New password is required"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
'''