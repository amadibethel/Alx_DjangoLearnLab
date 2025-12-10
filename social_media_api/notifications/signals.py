from django.db.models.signals import post_save
from django.dispatch import receiver
from attendees.models import Attendee
from .models import Notification

@receiver(post_save, sender=Attendee)
def notify_event_registration(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            recipient=instance.event.organizer,
            actor=instance.user,
            verb="registered for your event",
            target=instance.event
        )
