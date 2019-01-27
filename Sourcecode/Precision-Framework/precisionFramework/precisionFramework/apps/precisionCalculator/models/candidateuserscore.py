# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .. import managers
from . import Profile, Tool, Experiment, CandidatePair
import datetime
# Create your models here.

class CandidateUserScore(models.Model):
    CLONE_TYPE_1 = 1
    CLONE_TYPE_2 = 2
    CLONE_TYPE_3 = 3
    CLONE_TYPE_4 = 4

    # Relations
    experiment =  models.ForeignKey(Experiment)
    user = models.ForeignKey(Profile)
    candidate = models.ForeignKey(CandidatePair)
    # Attributes - Mandatory
    time_spent = models.PositiveIntegerField()
    clone_type =  models.CharField(max_length=200, blank=True, default="")
    vote = models.BooleanField()
    explaination = models.TextField(max_length=4000, default="", blank=True)
    # Attributes - Optional

    def __str__(self):
        return self.experiment
