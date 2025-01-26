from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

# Create your views here.

class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
       
    
    # def list(self,request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer_data = self.get_serializer(queryset, many=True)
    #     return Response(serializer_data.data, status=status.HTTP_200_OK)
        
        
        
    def perform_create(self, serializer):
       user=  serializer.save(is_active=True)
       refresh = RefreshToken.for_user(user)
       self.token_response = {
        
               "refresh":str(refresh),
               "access":str(refresh.access_token),
               "user": UserSerializer(user).data
           }
       
       
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(self.token_response, status=status.HTTP_201_CREATED)
    
        
        
class UserRetrieveUpdateDestyroAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        
        return CustomUser.objects.filter(id=self.request.user.id)
        
    
    #follow and unfollow dunctionality
class FollowView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request, user_id):
        #expecting userID from frontend
        user_to_follow = CustomUser.objects.get(id = user_id)
        
        request.user.is_following.add(user_to_follow)
        user_to_follow.followed_by.add(request.user)
        
        
        return Response(
            { "message": f"You are following new user {user_to_follow.username}"},
            status=status.HTTP_202_ACCEPTED
          )
        
        
        
        
        
class UnfollowView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self,request, user_id):
        user_to_unfollow = CustomUser.objects.get(id=user_id)
        
        
        request.is_following.remove(user_to_unfollow)
        user_to_unfollow.followed_by.remove(request.user)
        return Response(
            { "message": f"You are unfollowing new user {user_to_unfollow.username}"},
            status=status.HTTP_202_ACCEPTED
          )