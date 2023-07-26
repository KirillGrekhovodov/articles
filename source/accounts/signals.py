import os
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=get_user_model())
def pre_save_image(sender, instance, *args, **kwargs):
    if instance.pk:
        avatar = sender.objects.get(id=instance.id).profile.avatar
        if avatar:
            old_img = avatar.path
            new_avatar = instance.profile.avatar
            if new_avatar and new_avatar.path != old_img or not new_avatar:
                if os.path.exists(old_img):
                    os.remove(old_img)


