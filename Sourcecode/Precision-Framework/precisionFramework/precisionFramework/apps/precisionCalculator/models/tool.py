# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .. import managers
from . import Profile
# Create your models here.


class Tool(models.Model):
    # Relations
    user =  models.ForeignKey(Profile)

    # Attributes - Mandatory
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    # Attributes - Optional
    description = models.TextField(max_length=1000,default="",blank=True)
    webpage = models.URLField(
        max_length=2000,
        verbose_name=_("Webpage URL of this tool."),
        default="",
        blank=True
    )

    # Object Manager
    objects = managers.ToolManager

    # Meta and String
    class Meta:
        verbose_name = _("Tool")
        verbose_name_plural = _("Tools")
        ordering = ("name",)
        unique_together = ('name', 'version',)

    def __str__(self):
        return self.name + " "+ self.version