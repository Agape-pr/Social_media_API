from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsAuthorReadOnly
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from django.db.models import Q
from rest_framework.response import Response

from .models import Like

from django.shortcuts import get_object_or_404
from rest_framework import status
from .utils import create_notification

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
        
        create_notification(
            
            recipient=post.author,
            actor= self.request.user,
            verb="comment",
            target_object=post
              
        )
        serializer.save(author=self.request.user, post=post) 
        # Associate the post and user (author) when saving
        
    
    
    
class FeedView(APIView):
    
    def get(self,request):
        
        following_users = request.user.is_following.all()
        
        following_users_posts = Post.objects.filter(Q(author__in =following_users )).order_by('-created_at')
        
        serializer = PostSerializer(following_users_posts, many=True)
        
        return Response(serializer.data)
    
    
class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,post_id):
        
        post = get_object_or_404(Post, id=post_id)
        
        user = request.user
        like , created = Like.objects.get_or_create(post=post, user=user)
        
        if created:
            create_notification(
                recipient=post.author,
                actor = user,
                verb = "like",
                target_object= post
            )
            return Response(
                {"message": "post is liked"}, status=status.HTTP_201_CREATED
            )
        return Response({"message": "post already liked"}, status=status.HTTP_200_OK)
    
    
    
class UnLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request,post_id):
        
        post = get_object_or_404(Post, id = post_id)
        user = request.user
        like= Like.objects.get(post=post,user=user)
        like.delete()
        
        return Response({"message": "post is unliked"}, status=status.HTTP_200_OK)
        