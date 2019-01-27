from __future__ import unicode_literals

from django.db import models

from . import Profile
from django.utils.translation import ugettext_lazy as _


class CeleryTask(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    owner = models.ForeignKey(Profile)
    content_type = models.CharField(max_length=400)
    content = models.CharField(max_length=128)
    date_issued = models.DateTimeField()

    # Meta and String
    class Meta:
        verbose_name = _("CeleryTask")
        verbose_name_plural = _("CeleryTasks")

    def __str__(self):
        return "{task_id},{owner},{content_type},{content_type},{date_issued}".format(task_id=self.task_id,
                                                                                      owner=self.owner,
                                                                                      content_type=self.content_type,
                                                                                      content=self.content,
                                                                                      date_issued=self.date_issued)
