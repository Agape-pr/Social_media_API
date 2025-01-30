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
    