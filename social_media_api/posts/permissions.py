from .models import Post

from rest_framework.permissions import BasePermission

class IsAuthorReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        if request.method in ['PUT','PATCH','DELETE']:
            return obj.author == request.user
        
        
        return False
            