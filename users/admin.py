
from django.contrib import admin

from .models import User, Profile, Experience, Education, Feed, Skills, FollowRequest

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Feed)
admin.site.register(Skills)
admin.site.register(FollowRequest)


# Register your models here.
