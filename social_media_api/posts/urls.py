from django.urls import path, include
from .views import PostViewSet,CommentViewSet, FeedView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'post',PostViewSet,basename='posts') #CRUD FOR POSTS
router.register(r'comment', CommentViewSet, basename='comments')#CRUD FOR COMMENT

urlpatterns = [
    path('',include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed_post'),
]


