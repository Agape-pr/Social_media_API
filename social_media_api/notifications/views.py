from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

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
