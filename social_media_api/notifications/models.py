from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# In a new app called notifications, create a Notification model 
# with fields like recipient (ForeignKey to User), actor (ForeignKey to User), 
# verb (describing the action), target (GenericForeignKey to the object), and timestamp.

class Notification(models.Model):
    recipient = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='notifications')
    actor = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name='actions')
    verb = models.CharField(max_length=255)
    
    
    
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type','target_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} for {self.recipient}"
