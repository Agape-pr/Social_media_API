from django.urls import path, include
from .views import PostViewSet,CommentViewSet, FeedView, LikeView,UnLikeView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'post',PostViewSet,basename='posts') #CRUD FOR POSTS
router.register(r'comment', CommentViewSet, basename='comments')#CRUD FOR COMMENT

urlpatterns = [
    path('',include(router.urls)),
    
    path('feed/', FeedView.as_view(), name='feed_post'),
    path('posts/<int:post_id>/like/', LikeView.as_view(), name='like'),
    path('posts/<int:post_id>/unlike/', UnLikeView.as_view(), name='unlike'),
    
    # In notifications/urls.py, set up a route for users to view their notifications, like /notifications/.
    
]


