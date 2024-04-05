from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateTimeField(blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Profile: {self.user.username}'


# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     news = models.ForeignKey('News', on_delete=models.CASCADE)  # Предположим, что у вас будет модель для новостей
#
#
# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     news = models.ForeignKey('News', on_delete=models.CASCADE)
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
