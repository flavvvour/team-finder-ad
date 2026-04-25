import random
from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont


AVATAR_COLORS = [
    "#4A90D9", "#7B68EE", "#5CB85C", "#F0AD4E",
    "#D9534F", "#5BC0DE", "#9B59B6", "#1ABC9C",
    "#E67E22", "#3498DB", "#27AE60", "#C0392B",
]


def _generate_avatar_image(letter: str) -> ContentFile:
    size = (200, 200)
    bg_color = random.choice(AVATAR_COLORS)
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    text = (letter[0] if letter else "?").upper()

    font = None
    for font_path in (
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            font = ImageFont.truetype(font_path, 110)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default(size=80)

    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size[0] - w) / 2 - bbox[0]
    y = (size[1] - h) / 2 - bbox[1]
    draw.text((x, y), text, fill="white", font=font)

    buf = BytesIO()
    img.save(buf, format="PNG")
    return ContentFile(buf.getvalue())


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    phone = models.CharField(max_length=12, unique=True, blank=True, null=True, default=None)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
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
            img_content = _generate_avatar_image(letter)
            safe_email = self.email.replace("@", "_").replace(".", "_")
            self.avatar.save(f"avatar_{safe_email}.png", img_content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"
