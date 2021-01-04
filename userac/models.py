from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userimg = models.ImageField(upload_to = "media/profile", blank=True)
    bio = models.CharField(max_length=200, blank=True)
    following = models.IntegerField(default=0)
    followed = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}"

class Allposts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="media/posts", blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} created a post @ {self.date.date()}"


class Like(models.Model):
    user = models.ManyToManyField(User, related_name="likinguser")
    post = models.OneToOneField(Allposts, on_delete=models.CASCADE)

    @classmethod
    def like(cls, post, liking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.add(liking_user)

    @classmethod
    def dislike(cls, post, liking_user):
        obj, create = cls.objects.get_or_create(post=post)
        obj.user.remove(liking_user)
    
    def __str__(self):
        return f"{self.user} liked {self.post}"

class Allcomment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented_user")
    post = models.ForeignKey(Allposts, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} commented on {self.post}"

class Follow_Unfollow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed = models.ManyToManyField(User, related_name="followed", blank=True)
    follower = models.ManyToManyField(User, related_name="follower", blank=True)

    def __str__(self):
        return f"{self.user} followed {self.followed}"

    def get_followed(self):
        return self.followed

    @classmethod
    def follow(cls, user, to_user):
        obj, create = cls.objects.get_or_create(user = user)
        obj.followed.add(to_user)


    @classmethod
    def unfollow(cls, user, to_user):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.remove(to_user)
    
    @classmethod
    def add_follower(cls, user, to_user):
        obj, create = cls.objects.get_or_create(user=user)
        obj.follower.add(to_user)

    @classmethod
    def remove_follower(cls, user, to_user):
        obj, create = cls.objects.get_or_create(user=user)
        obj.follower.remove(to_user)