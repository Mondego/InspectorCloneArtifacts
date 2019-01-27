# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .. import managers
from . import Block


# Create your models here.

class CandidatePair(models.Model):
    STATUS_FALSE = 0
    STATUS_TRUE = 1
    STATUS_UNDECIDED = 2
    # RULE: block with less tokens is candidate_one. If tokens are same, block with lower bcb_function_id is candidate_one.
    candidate_one = models.ForeignKey(Block, related_name="candidate_one")
    candidate_two = models.ForeignKey(Block, related_name="candidate_two")
    true_positive_count = models.PositiveSmallIntegerField(default=0)
    false_positive_count = models.PositiveSmallIntegerField(default=0)
    confirmed_status = models.PositiveSmallIntegerField(default=STATUS_UNDECIDED)
    type_one_count = models.PositiveSmallIntegerField(default=0)
    type_two_count = models.PositiveSmallIntegerField(default=0)
    type_three_count = models.PositiveSmallIntegerField(default=0)
    type_four_count = models.PositiveSmallIntegerField(default=0)

    USER_SOURCE_TYPE = 0 # user
    PRECISION_FRAMEWORK_SOURCE_TYPE = 1 # PF
    BCB_SOURCE_TYPE = 2 # BCB

    source_type = models.PositiveSmallIntegerField(default=PRECISION_FRAMEWORK_SOURCE_TYPE)

    class Meta:
        verbose_name = _("CandidatePair")
        verbose_name_plural = _("CandidatePairs")

    def __str__(self):
        return "{c1},{c2}".format(c1=self.candidate_one, c2=self.candidate_two)
