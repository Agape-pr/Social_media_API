objects = CustomUserManager()
def __str__(self):
    return self.username


  -----define custom user manager to handle user reigistartion.---------


class CustomUserManager(BaseUserManager):
def create_user(self,username, password=None, **extra_fields):
    if not username:
        raise ValueError("username should be provided")
    if not password:
        raise ValueError("Password should be provided")
    
    user = self.model(username=username,**extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault('is_active', True)
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser',True)
    superuser = self.create_user(username, password,**extra_fields)
    return superuser


----next---
define serializers , include password field , set it as writte only


handle views .... following drf







handle urls.... 
include token authentication from the rest_framework_simplejwt.views import tokenobtainpairview
