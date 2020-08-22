from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Relation(models.Model):
    followed = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='follows')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.PROTECT, related_name='postsByUSer')
    postcontent = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    likedBy = models.ManyToManyField('User', default=None, blank=True, related_name='likesByUser')

    @property
    def likes(self):
        return self.likedBy.all().count()

    def __str__(self):
        return f"{self.pk}: ({self.likes}) {self.postcontent} by {self.username} at {self.timestamp}"


