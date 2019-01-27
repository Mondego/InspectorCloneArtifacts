# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .. import managers
from . import Profile
# Create your models here.


class Judge(models.Model):
    # Relations
    user =  models.ForeignKey(Profile)

    # Attributes - Mandatory
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)


    # Object Manager
    objects = managers.ProfileManager

    # Meta and String
    class Meta:
        verbose_name = _("Tool")
        verbose_name_plural = _("Tools")
        ordering = ("name",)

    def __str__(self):
        return self.user.username