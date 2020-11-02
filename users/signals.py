import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile, Experience, Education, Feed, Skills, FriendRequest


@receiver(post_save, sender=Profile)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def save_profile(sender, instance, **kwargs):
    instance.objects.save()


@receiver(post_save, sender=Experience)
def create_or_update_user_experience(sender, instance, created, **kwargs):
    if created:
        Experience.objects.create(user=instance)


@receiver(post_save, sender=Experience)
def save_experience(sender, instance, **kwargs):
    Experience.objects.save()


@receiver(post_save, sender=Education)
def create_or_update_user_education(sender, instance, created, **kwargs):
    if created:
        Education.objects.create(user=instance)


@receiver(post_save, sender=Education)
def save_education(sender, instance, **kwargs):
    Education.objects.save()


@receiver(post_save, sender=Feed)
def create_or_update_user_feed(sender, instance, created, **kwargs):
    if created:
        Feed.objects.create(user=instance)


@receiver(post_save, sender=Feed)
def save_feed(sender, instance, **kwargs):
    Feed.objects.save()


@receiver(post_save, sender=Skills)
def create_or_update_user_skills(sender, instance, created, **kwargs):
    if created:
        Skills.objects.create(user=instance)


@receiver(post_save, sender=Skills)
def save_skills(sender, instance, **kwargs):
    Skills.objects.save()


@receiver(post_save, sender=FriendRequest)
def create_or_update_user_friend_request(sender, instance, created, **kwargs):
    if created:
        FriendRequest.objects.create(user=instance)


@receiver(post_save, sender=FriendRequest)
def save_friend_request(sender, instance, **kwargs):
    FriendRequest.objects.save()







