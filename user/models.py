from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    date = models.DateTimeField(auto_now_add=True)
    context = models.TextField()

    def __str__(self):
        return f'{self.context}'

    class Meta:
        ordering = ['-date']
        app_label = 'user'