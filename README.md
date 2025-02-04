# Social Media API - README

## Overview
The **Social Media API** is built using Django and Django REST Framework (DRF) to provide user authentication and profile management functionalities. It includes features like user registration, login, token-based authentication, and profile management.

## Features
- User Registration
- User Login with Token Authentication
- User Profile Management
- User Post (CRUD OPRATIONS)
- User Comment (CRUD OPERATIONS)
- Followers System
- Feed posts
- Notifications system
- Secured API Endpoints

## Technologies Used
- Python 
- Django
- Django REST Framework
- SQLite (default)
- Postman (for API testing)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool ('used 'myvenv' as for virtual environment name)

## Installation & Setup

### Step 1: Environment Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv myvenv
     venv/Scripts/activate  # On Windows use: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
    - pip install django
    - pip installdjangorestframework 
    - pip install djangorestframework-authtoken
   ```
3. Create a new Django project:
   ```bash
   django-admin startproject social_media_api
   ```
4. create app named `accounts`:
   ```bash
   cd social_media_api
   python manage.py startapp accounts
   ```
5. Add the following to `INSTALLED_APPS` in `settings.py`:
   ```python
   INSTALLED_APPS = [
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'rest_framework',
       'rest_framework.authtoken',
       'accounts',
   ]
   ```
6. Run migrations:
   ```bash
   python manage.py migrate
   ```

## Step 2: Configure User Authentication
1. Create a custom user model extending `AbstractUser` and add the following fields:
   - `bio`
   - `profile_picture`
   - `followers` (ManyToMany field referencing itself, `symmetrical=False`)

2. Update `settings.py` to use the custom user model:
   ```python
   AUTH_USER_MODEL = 'accounts.CustomUser'
   ```
3. Implement views and serializers in the `accounts` app for:
   - User registration(used listcreateAPI VIEW FROM RESTFUL GENERICS)
   after user is registered , it has return acess token , 
     * import token_ refresh from rest_framework_simplejwt.tokens
     * override  the perform_create method and include the logic for token:

       # def perform_create(self, serializer):
            user=  serializer.save(is_active=True)
            refresh = RefreshToken.for_user(user)
            self.token_response = {
                
                    "refresh":str(refresh),
                    "access":str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
     * override the create method , to return token 
        # def create(self, request, *args, **kwargs):
            super().create(request, *args, **kwargs)
            return Response(self.token_response, status=status.HTTP_201_CREATED)
   - Login
   - Token retrieval

## Step 3: Define API Endpoints
1. Configure URL patterns in `accounts/urls.py`:
   ```python
   from django.urls import path
   from .views import RegisterView, LoginView, ProfileView

   urlpatterns = [
       path('register/', RegisterView.as_view(), name='register'),
       
       # for login , needed importation: from rest_framework_simplejwt.views import TokenObtainPairView
            path('login/',TokenObtainPairView.as_view(), name='login-token'), #since we need login to return the access token
       path('profile/', ProfileView.as_view(), name='profile'),
   ]
   ```



# Documentation for Posts and Comments API

## Models

### Post Model
Represents a blog post created by a user.

- `author`: ForeignKey to User model (author of the post).
- `title`: CharField with a max length of 255 characters.
- `content`: TextField for the body of the post.
- `created_at`: Auto-generated DateTime when the post is created.
- `updated_at`: Auto-generated DateTime when the post is updated.

### Comment Model
Represents a comment on a post by a user.

- `post`: ForeignKey to Post model (the post being commented on).
- `author`: ForeignKey to User model (author of the comment).
- `content`: TextField containing the comment text.
- `created_at`: Auto-generated DateTime when the comment is created.
- `updated_at`: Auto-generated DateTime when the comment is updated.

## Views

### PostViewSet
Handles CRUD operations for posts.

_ import viewsets from restframework: 
from rest_framework import viewsets
- `list`: Retrieve all posts.: 
- `create`: Create a new post.
- `retrieve`: Get details of a specific post.
- `update`: Update an existing post.
- `partial_update`: Partially update a post.
- `destroy`: Delete a post.
# -- code---
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title','content']
    
    
    
    def perform_create(self,serializer):
        
        serializer.save(author=self.request.user)
# --- code ----

### CommentViewSet
Handles CRUD operations for comments.

- `list`: Retrieve all comments for a specific post.
- `create`: Add a comment to a post.
- `retrieve`: Get details of a specific comment.
- `update`: Update an existing comment.
- `partial_update`: Partially update a comment.
- `destroy`: Delete a comment.

# ---code----:
 
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


# ---code---

## define a custom persmisson file . for logic to limit user to delete or update post or comment if not owner.
        # permission.py file:
        
# ---code ---
    from .models import Post

    from rest_framework.permissions import BasePermission

    class IsAuthorReadOnly(BasePermission):
        
        def has_object_permission(self, request, view, obj):
            if request.method in ['GET', 'HEAD', 'OPTIONS']:
                return True
            
            if request.method in ['PUT','PATCH','DELETE']:
                return obj.author == request.user
            
            
            return False

# --- code ----
HANDLE THE VIEWS: 



# Documentation for user follows and feed functionality.

1. modify the customuser model to include following and followers fields:
    $followers = models.ManyToManyField('self',symmetrical=False,blank=True, related_name='followed_by')
    following = models.ManyToManyField('self',symmetrical=False,blank=True, related_name='is_following')

    REASEON: This means that each user can be related to other users within the same model, which is exactly what a "following" or "follower" relationship represents.
    #SYMETRICAL FALSE: This means the relationship is not mutual by default. For instance, if User A follows User B, User B does not automatically follow User A.


2. followView and UnFollowVIew(APIView)
    *  override post method:
        (this receives post_id from frontend):
        $
        user_to_follow = CustomUser.objects.get(id = user_id)
        
        request.user.is_following.add(user_to_follow)
        user_to_follow.followed_by.add(request.user)


    * for unfollow:
        $
       user_to_unfollow = CustomUser.objects.get(id=user_id)

        request.user.is_following.remove(user_to_unfollow)
        user_to_unfollow.followed_by.remove(request.user)



# feed Functinality
     

     # -- codes ---

    ```python

     def get(self,request):
        
        following_users = request.user.is_following.all()
        
        following_users_posts = Post.objects.filter(Q(author__in =following_users )).order_by('-created_at')
        
        serializer = PostSerializer(following_users_posts, many=True)
        
        return Response(serializer.data)
    

# define urls ....
path('feed/', FeedView.as_view(), name='feed_post'),
path('posts/<int:post_id>/like/', LikeView.as_view(), name='like'),
path('posts/<int:post_id>/unlike/', UnLikeView.as_view(), name='unlike'),


# Social Media API - Follow System and Feed Feature

## Overview
This part outlines the new features added to the Social Media API: the ability for users to follow other users and view an aggregated feed of posts from users they follow.

## 1. User Model Updates
The `CustomUser` model has been updated to support user relationships for following and followers. The following changes made:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    followers = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='followed_by'
    )
    following = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='is_following'
    )
```

### Fields explanation:
- `followers`: Represents users who follow the current user.
- `following`: Represents users that the current user follows.
- `symmetrical=False`: Ensures that following someone does not mean they automatically follow back.

## 2. API Endpoints

### 2.1 Follow a User
- **URL**: `/follow/<int:user_id>/`
- **Method**: `POST`
- **Permissions**: Must be authenticated.
- **Description**: Allows an authenticated user to follow another user by their ID.
- **Example Request:**
  ```http
  POST /follow/2/
  ```
- **Example Response:**
  ```json
  {
    "detail": "User followed successfully"
  }
  ```

### 2.2 Unfollow a User
- **URL**: `/unfollow/<int:user_id>/`
- **Method**: `POST`
- **Permissions**: Must be authenticated.
- **Description**: Allows an authenticated user to unfollow another user by their ID.
- **Example Request:**

  ```http
  POST /unfollow/2/
  ```
- **Example Response:**
  ```json
  {
    "detail": "User unfollowed successfully"
  }
  ```

### 2.3 Get User Feed
- **URL**: `/feed/`
- **Method**: `GET`
- **Permissions**: Must be authenticated.
- **Description**: Retrieves an aggregated feed of posts from users that the authenticated user follows, ordered by creation date.
- **Example Request:**
  ```http
  GET /feed/
  ```
- **Example Response:**
  ```json
  [
    {
      "id": 1,
      "user": 2,
      "content": "Post content",
      "created_at": "2025-02-01T12:00:00Z"
    },
    {
      "id": 2,
      "user": 3,
      "content": "Another post",
      "created_at": "2025-02-01T10:30:00Z"
    }
  ]
  ```

## 3. URL Configuration
Ensure these URLs are added to `accounts/urls.py` and `posts/urls.py`:

```python
from django.urls import path
from .views import follow_user, unfollow_user

urlpatterns = [
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
]
```

For the feed in `posts/urls.py`:
```python
from django.urls import path
from .views import user_feed

urlpatterns = [
    path('feed/', user_feed, name='user-feed'),
]
```



## like functionality logic.


```python 
    

"" first define model like. : define two fields(post and user) with foreign key to post model and customuser model respectively


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
        

```
###  Notification functionality documentation.
 define notification model .
2. make util file to house the function to handle notification which later will be imported at each view , where we need to remain with notification.

## Notification model

```python
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType  # this cross control all models in project
from django.contrib.contenttypes.fields import GenericForeignKey # this connect two fields together for target field
 
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



```
# make util five to handle the request , with method.
```python

from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

def create_notification(recipient,actor,verb, target_object):
    target_content_type = ContentType.objects.get_for_model(target_object)
    
    notification = Notification.objects.create(
        recipient = recipient,
        actor = actor,
        verb = verb,
        target_content_type = target_content_type,
        target_object_id = target_object.id,
        target  = target_object
    )
    return notification
```
## import function in view, whenever we want to remain with notification

```python 
create_notification(
            
            recipient=post.author,
            actor= self.request.user,
            verb="comment",
            target_object=post
              
        )

````
## to generate comment.

```python
class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Fetch notifications for the authenticated user.
        Unread notifications are shown first.
        """
        user = request.user
        # Separate unread and read notifications
        unread_notifications = Notification.objects.filter(recipient=user, read=False).order_by('-timestamp')
        read_notifications = Notification.objects.filter(recipient=user, read=True).order_by('-timestamp')
        
        # Serialize the notifications
        unread_serializer = NotificationSerializer(unread_notifications, many=True)
        read_serializer = NotificationSerializer(read_notifications, many=True)

        return Response({
            "unread_notifications": unread_serializer.data,
            "read_notifications": read_serializer.data
        })
```
# view to set notification to read , automatically , which receives the ids , from the frontend side after getting opened.


```python 
class MarkNotificationAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Mark specific notifications as read.
        Expects a list of notification IDs in the request body.
        """
        notification_ids = request.data.get('notification_ids', [])
        notifications = Notification.objects.filter(recipient=request.user, id__in=notification_ids)

        updated_count = notifications.update(read=True)  # Update read status
        return Response({"message": f"{updated_count} notifications marked as read."})
````
