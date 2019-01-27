# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .. import managers
# Create your models here.


class Profile(models.Model):
    # Relations
    # related_name  is used to define how can you access a profile instance from the user model.
    # For example, if myuser is a User instance, you can access its profile with myprofile = myuser.profile
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name = "profile",
        verbose_name = _("User")
    )
    # Attributes - Mandatory
    vote_count = models.PositiveIntegerField(
        default=0,
        verbose_name = _("Number of votes casted by this user. Counts are meausred for completed experiments only.")
    )

    # Attributes - Optional
    is_expert = models.BooleanField(
        default=False,
        verbose_name=_("If true, this user has been validated by Mondego group as an expert on Software Clones."),
        blank=True
    )
    is_Validatd = models.BooleanField(
        default=False,
        verbose_name=_("If true, a validation process has been conducted on this user."),
        blank=True
    )
    webpage = models.URLField(
        max_length=2000,
        verbose_name=_("Webpage URL of this user."),
        default="",
        blank=True
    )
    # Object Manager
    objects = managers.ProfileManager()

    # Custom Properties
    @property
    def username(self):
        return self.user.username

    # Methods

    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()