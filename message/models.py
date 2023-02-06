from datetime import timezone

from django.db import models

from accounts.models import CustomUser


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def mark_as_read(self):
        self.read_at = timezone.now()
        self.save()

    def mark_as_deleted(self):
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.subject
