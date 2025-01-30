from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestyroAPIView, FollowView, UnfollowView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    
    path('register/', UserListCreateView.as_view(), name='register'),
    path('login/',TokenObtainPairView.as_view(), name='login-token'),
    path('profile/<int:pk>/', UserRetrieveUpdateDestyroAPIView.as_view(), name='profile'),
    
    path('follow/<int:user_id>/', FollowView.as_view(), name='add_followers'),
    path('unfollow/<int:user_id>/', UnfollowView.as_view(), name='remove_follow'),
   

]
