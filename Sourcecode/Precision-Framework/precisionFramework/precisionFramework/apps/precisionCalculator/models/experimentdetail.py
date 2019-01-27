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

class ExperimentDetail(models.Model):
    USER_SOURCE_TYPE = 0
    PRECISION_FRAMEWORK_SOURCE_TYPE = 1
    BCB_SOURCE_TYPE = 2

    SOURCE_TYPE = (
        (USER_SOURCE_TYPE, 'USER'),
        (PRECISION_FRAMEWORK_SOURCE_TYPE, 'PF'),
        (BCB_SOURCE_TYPE, 'BCB'),
    )
    AUTO_T1 = "AUTO_T1"
    ADDED_T2 = "ADDED_T2"
    AUTO_T2 = "AUTO_T2"
    AUTO_T3_1 = "AUTO_T3_1"
    # Relations
    experiment =  models.ForeignKey(Experiment)
    candidate_pair = models.ForeignKey(CandidatePair)
    # Attributes - Mandatory
    source_type = models.PositiveSmallIntegerField(choices=SOURCE_TYPE, default=USER_SOURCE_TYPE)
    vote = models.BooleanField()
    clone_type = models.FloatField(default=0)
    resolution_method = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(Profile, null=True)
    visited = models.BooleanField(default=False)
    # Attributes - Optional

    # Object Manager
    objects = managers.ExperimentActionManager()
    def __str__(self):
        return self.experiment

