from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Message(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    def __str__(self):
        # Display username and first 20 characters of the message
        return f"{self.poster.username}: {self.content[:20]}"

