*** custome usermodel ***
filds: usernamem bio and profile pic, 
*for profile picture remember to include uploaad_to property , which is a folder where , images will be saved.
*followers , which is symetrical to the user, set symentrical = true, include self also .
meaning of symetrical: manyto many relationship allow modela to have relationshipn top other models or itself
"The field references 'self' because it connects a user to other users within the same model."
codes----
#followers = models.ManyToManyField('self', symmetrical=False, related_name='following')

the whole codes: 
 #class CustomUser(AbstractUser):
    bio = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='images', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
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