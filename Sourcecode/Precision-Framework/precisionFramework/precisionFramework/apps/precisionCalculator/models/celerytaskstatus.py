from __future__ import unicode_literals

from django.db import models

class DjCeleryTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    hidden = models.IntegerField()
    meta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'