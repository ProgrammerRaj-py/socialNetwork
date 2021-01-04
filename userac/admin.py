from django.contrib import admin
from .models import Allposts, Like, Allcomment, Follow_Unfollow, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Allposts)
admin.site.register(Like)
admin.site.register(Allcomment)
admin.site.register(Follow_Unfollow)