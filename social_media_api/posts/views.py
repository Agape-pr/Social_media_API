from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsAuthorReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView


from django.db.models import Q
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title','content']
    
    
    
    def perform_create(self,serializer):
        
        serializer.save(author=self.request.user)
    
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorReadOnly]
    
    
    def perform_create(self,serializer):
        # 1. Get the post ID from the request data
        post_id = self.request.data.get('post')  # Expecting 'post' to be included in the POST request
        
        # 2. Fetch the related Post instance. If post does not exist, raise a 404 error.
        post = get_object_or_404(Post, id=post_id)  # Fetch Post using the post_id
        
        # 3. Save the new comment with the author and post associations
        serializer.save(author=self.request.user, post=post)  # Associate the post and user (author) when saving
        
    
    
    
class FeedView(APIView):
    
    def get(self,request):
        
        following_users = request.user.is_following.all()
        
        following_users_posts = Post.objects.filter(Q(author__in =following_users )).order_by('-createed_at')
        
        serializer = PostSerializer(following_users_posts, many=True)
        
        return Response(serializer.data)
        