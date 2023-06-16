from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BaseMessage(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    context = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.context}"

    class Meta:
        ordering = ["-date"]
        abstract = True


class Message(BaseMessage):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )

    class Meta:
        app_label = "user"


class MessageAnswer(BaseMessage):
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="message_answer"
    )

    class Meta:
        app_label = "user"
