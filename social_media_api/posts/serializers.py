from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Post
        fields = ['id', 'title','content','author', 'created_at', 'updated_at']#make author readonly
        read_only_fields = ['author', 'created_at','updated_at']
        
    def validate_title(self,value):
        if len(value)>20:
            raise serializers.ValidationError('Title should not be greated than 20 characters')
        return value
        
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','content','author','created_at','updated_at','post']
        read_only_fields = ['author', 'created_at','updated_at']