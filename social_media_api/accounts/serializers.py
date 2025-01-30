from .models import CustomUser
from rest_framework import serializers

from django.contrib.auth.hashers import make_password
#for hashing password


class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True) 
    following = serializers.PrimaryKeyRelatedField(many=True, read_only= True)
    followers = serializers.PrimaryKeyRelatedField(many=True, read_only = True)
    
    class Meta:
        
        model = CustomUser
        
        fields = ['id','username','bio','profile_picture','password','following', 'followers']
        read_only_fields = ['following', 'followers']
        
    def create(self, validated_data):
             # Hash the password explicitly before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
        
            