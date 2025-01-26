
from django.db import models
from django.contrib.auth import get_user_model





# In a new app within the project called posts, create models for Post and Comment.
# Post should have fields like author (ForeignKey to User), title, content, created_at, and updated_at.
# Comment should reference both Post (ForeignKey) and User (author), with additional fields for content, 
# created_at, and updated_at.

class Post(models.Model):
    title = models.CharField(max_length=400)
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name='posts')
    
def __str__(self):
    return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name='user_comment')
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    
    
