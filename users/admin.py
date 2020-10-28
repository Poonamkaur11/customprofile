from django.contrib import admin

from .models import User, Profile, Experience, Education, Feed, Skills, FriendRequest

admin.site.register(User)

admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Feed)
admin.site.register(Skills)
admin.site.register(FriendRequest)

admin.site.register(Profile)




# Register your models here.
