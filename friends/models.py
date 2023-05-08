from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendship_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friendship_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=(
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ), default='pending', max_length=10)