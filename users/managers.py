from django.contrib.auth.base_user import BaseUserManager

from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class ProfileManager(BaseUserManager):
    pass


class BaseModelManager(BaseUserManager):
    pass


class Feed(BaseUserManager):
    pass


class Skills(BaseUserManager):
    pass


class Follow(BaseUserManager):

    def follow(self, user_to_follow):
        obj, created = self.objects.get_or_create(user=self)
        return self.user.following.add(self, user_to_follow)

    def unfollow(self, user, user_to_unfollow):
        obj, created = self.objects.get_or_create(user=user)
        return self.following.remove(user, user_to_unfollow)
