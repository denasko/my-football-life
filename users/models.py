from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Profile: {self.user.username}'


class Feedback(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    header = models.CharField(max_length=200)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return f'Feedback: {self.profile.user.username}, оценка - {self.rating}'

#
#
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
