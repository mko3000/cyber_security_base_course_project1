from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Display username and first 20 characters of the message
        return f"{self.poster.username}: {self.content[:20]}"

