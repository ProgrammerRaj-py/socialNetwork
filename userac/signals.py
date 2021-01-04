from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from userac.models import Follow_Unfollow

@receiver(m2m_changed, sender = Follow_Unfollow.followed.through)
def add_follower(sender, instance, action, reverse, pk_set, **kwargs):
    followed_user = []
    logged_user = User.objects.get(username= instance)
    for i in pk_set:
        user = User.objects.get(pk = i)
        following_obj = Follow_Unfollow.objects.get(user=user)
        followed_user.append(following_obj)

    if action == "pre_add":
        for i in followed_user:
            i.follower.add(logged_user)
            i.save()
    
    if action == "pre_remove":
        for i in followed_user:
            i.follower.remove(logged_user)
            i.save()

    