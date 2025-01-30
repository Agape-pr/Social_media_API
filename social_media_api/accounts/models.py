from django.db import models
from django.contrib.auth.models  import AbstractUser , BaseUserManager
from django.contrib.auth import get_user_model
# Create your models here.




class CustomUserManager(BaseUserManager):
    def create_user(self,username, password=None, **extra_fields):
        if not username:
            raise ValueError("username should be provided")
        if not password:
            raise ValueError("Password should be provided")
        # extra_fields.setdefault('is_active', True) 
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)
        superuser = self.create_user(username, password,**extra_fields)
        return superuser
    
    
    
class CustomUser(AbstractUser):
    bio = models.CharField(max_length=200)
    
    
    profile_picture = models.ImageField(upload_to='images', blank=True, null=True)
    followers = models.ManyToManyField('self',symmetrical=False,blank=True, related_name='followed_by')
    following = models.ManyToManyField('self',symmetrical=False,blank=True, related_name='is_following')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    
    
    objects = CustomUserManager()
    def __str__(self):
        return self.username
    
    
    



    
    
    