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

class ExperimentJudge(models.Model):
    STATUS_NOT_STARTED = 0
    STATUS_STARTED = 1
    STATUS_COMPLETED = 2

    STATUS = (
        (STATUS_STARTED, 'STARTED THE EXPERIMENT'),
        (STATUS_NOT_STARTED, 'NOT STARTED THE EXPERIMENT'),
        (STATUS_COMPLETED, 'COMPLETED THE EXPERIMENT'),
    )
    # Relations
    experiment =  models.ForeignKey(Experiment)
    user = models.ForeignKey(Profile)
    #current_pair = models.ForeignKey(CandidatePair)
    # Attributes - Mandatory
    status = models.PositiveSmallIntegerField(choices=STATUS, default=STATUS_NOT_STARTED)

    # Attributes - Optional

    def __str__(self):
        return self.experiment
