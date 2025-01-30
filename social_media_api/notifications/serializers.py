from rest_framework import serializers
from .models import Notification
from accounts.models import CustomUser  # Import your custom user model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]  # Ensure only necessary fields


#go deep in 
class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)  # Serialize recipient correctly
    actor = UserSerializer(read_only=True)  # Serialize actor correctly
    target = serializers.SerializerMethodField()  # Handle GenericForeignKey

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp', 'read']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']

    def get_target(self, obj):
        """
        Handle the serialization of the GenericForeignKey `target`.
        """
        if obj.target is None:
            return None
        
        if hasattr(obj.target, "id"):  # If target has an ID, return basic details
            return {
                "id": obj.target.id,
                "type": obj.target_content_type.model,
                "name": str(obj.target)  # This should return a readable string
            }
        
        return str(obj.target)  # Fallback to string representation
