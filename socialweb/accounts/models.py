from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


username_validator = UnicodeUsernameValidator()

class CustomUser(AbstractUser):
    user_description=models.TextField(blank=True,null=True)
    user_image=models.ImageField(upload_to='profile_images/')
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        primary_key=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    def __str__(self):
        return self.username
