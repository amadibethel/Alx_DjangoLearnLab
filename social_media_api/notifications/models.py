from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        related_name="notifications",
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        User,
        related_name="actions",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    verb = models.CharField(max_length=255)

    # Generic reference to any object (event, attendee, ticket, etc.)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey("content_type", "object_id")

    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target}"
