from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, UserProfile
from .serializers import (UserRegistrationSerializer, UserLoginSerializer, 
                         UserSerializer, UserProfileSerializer)

# Frontend registration view
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        phone_number = request.POST.get('phone_number')
        company_name = request.POST.get('company_name')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        
        if password != password2:
            messages.error(request, "Passwords don't match.")
            return render(request, 'registration/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'registration/register.html')
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                phone_number=phone_number,
                company_name=company_name if user_type == 'employer' else None,
                skills=skills if user_type == 'job_seeker' else None,
                experience=experience if user_type == 'job_seeker' else None
            )
            UserProfile.objects.create(user=user)
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'registration/register.html')
    
    return render(request, 'registration/register.html')

@api_view(['POST'])
@permission_classes([AllowAny])
def api_register_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Create user profile
        UserProfile.objects.create(user=user)
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logout successful'})

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user