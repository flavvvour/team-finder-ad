from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from constants import USER_ABOUT_MAX_LENGTH, USER_NAME_MAX_LENGTH, USER_PHONE_MAX_LENGTH

from users.managers import UserManager
from users.service import generate_avatar_image


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField(max_length=USER_NAME_MAX_LENGTH)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    phone = models.CharField(max_length=USER_PHONE_MAX_LENGTH, unique=True, blank=True, null=True, default=None)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=USER_ABOUT_MAX_LENGTH, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Variant 1: favourites
    favorites = models.ManyToManyField(
        "projects.Project",
        blank=True,
        related_name="interested_users",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            letter = self.name[0] if self.name else "?"
            img_content = generate_avatar_image(letter)
            safe_email = self.email.replace("@", "_").replace(".", "_")
            self.avatar.save(f"avatar_{safe_email}.png", img_content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"
