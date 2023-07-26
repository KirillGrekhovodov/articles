from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.

from django.contrib.auth import get_user_model


def get_url_path(instance, filename):
    return f"avatars/{instance.user.pk}/{filename}"


def validate_image_size(obj):
    filesize = obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(null=True, blank=True, upload_to=get_url_path, verbose_name='Аватар',
                               validators=[
                                   FileExtensionValidator(["jpg", "jpeg"], 'Корректные форматы файла ("jpg", "jpeg")'),
                                   validate_image_size])

    def __str__(self):
        return self.user.username + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class MyUser(AbstractUser):
    phone = models.CharField(max_length=15)
    subscribers = models.ManyToManyField(get_user_model(), related_name="who_is_subscribed_to")
    post_likes = models.ManyToManyField("webapp.Post", )
