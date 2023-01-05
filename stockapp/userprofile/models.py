import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        Profile.objects.create(owner=user)

        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.model(email=email, first_name=first_name, last_name=last_name)
        user.is_superuser = True
        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.last_name

    def __str__(self):
        return self.email


class Profile(models.Model):
    profileId = models.UUIDField(default=uuid.uuid4, primary_key=True)
    owner = models.ForeignKey(to=UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.get_full_name()



