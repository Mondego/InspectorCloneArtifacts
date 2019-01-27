# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from . import Profile, Tool
from .. import managers


# Create your models here.

def generate_filename(self, filename):
    d= timezone.now()
    time_stamp = string_i_want=('%02d_%02d_%02d_%d'%(d.hour,d.minute,d.second,d.microsecond))[:-4]
    file_path = "{media_root}/users/{username}/uploads/clonepairs/{year}_{month}_{day}/{time_stamp}/{filename}".format(
        media_root=settings.MEDIA_ROOT,
        username= self.user.username,
        year=d.year,
        month=d.month,
        day=d.day,
        time_stamp=time_stamp,
        filename=filename
    )
    return file_path

class Experiment(models.Model):
    SIMILARITY_TOKEN = 1
    SIMILARITY_LINE = 2
    SIMILARITY_AVG = 3
    SIMILARITY_BOTH = 0

    SIM_TYPE = (
        (SIMILARITY_BOTH, 'BOTH LINE AND TOKEN'),
        (SIMILARITY_TOKEN, 'TOKEN ONLY'),
        (SIMILARITY_LINE, 'LINE ONLY'),
        (SIMILARITY_AVG, 'AVERAGE OF LINE AND TOKEN'),
    )
    # Relations
    user =  models.ForeignKey(Profile)
    tool = models.ForeignKey(Tool)
    # Attributes - Mandatory
    validate_extension = FileExtensionValidator(allowed_extensions=["zip"])
    #validate_content = FileContentValidator(max_size=1024*1000*1000,min_size=0, username = user.user.username)
    clonepairs = models.FileField(upload_to=generate_filename,
                                  verbose_name=_("Upload Clonepairs file in zip format."),
                                  help_text=_("Please make sure there is only one file with .txt extension in "
                                              "the zip. Number of tokens>=50 clone pairs should be at least 100,000 "
                                              "for us to draw a random sample"),
                                  max_length=2000, validators=[validate_extension])
    upload_date = models.DateTimeField('date uploaded')
    # parameters for eexperiment
    similarity_type = models.PositiveSmallIntegerField(choices=SIM_TYPE, default=SIMILARITY_BOTH)
    mininum_similarity = models.PositiveSmallIntegerField(default=70)
    minimum_lines = models.PositiveSmallIntegerField(null=True, blank=True)
    maximum_lines = models.PositiveSmallIntegerField(null=True, blank=True)
    minimum_prity_printed_lines = models.PositiveSmallIntegerField(null=True, blank=True)
    maximum_prity_printed_lines = models.PositiveSmallIntegerField(null=True, blank=True)
    minimum_tokens = models.PositiveSmallIntegerField(null=True, blank=True)
    maximum_tokens = models.PositiveIntegerField(null=True, blank=True)
    minimum_judges = models.PositiveSmallIntegerField(null=True, blank=True)
    minimum_confidence = models.PositiveSmallIntegerField(null=True, blank=True)
    sampled_clonepairs = models.CharField(max_length=2000, null=True, blank=True)
    name = models.CharField(max_length=2000)
    is_locked = models.NullBooleanField(default=False, null=True, blank=True)



    # Attributes - Optional
    result_dump = models.CharField(max_length=4000, default="", blank=True,
                                   verbose_name=_("Location of the experiment's result file."))

    # Object Manager
    objects = managers.ExperimentManager

    # Meta and String
    class Meta:
        verbose_name = _("Experiment")
        verbose_name_plural = _("Experiments")

    def __str__(self):
        return self.name

