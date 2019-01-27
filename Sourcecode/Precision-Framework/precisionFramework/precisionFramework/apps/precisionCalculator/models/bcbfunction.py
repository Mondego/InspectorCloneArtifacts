from __future__ import unicode_literals

from django.db import models


class BCBFunctions(models.Model):
    use_db = 'bcb'

    name = models.CharField(db_column='NAME', max_length=400)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=200)  # Field name made lowercase.
    startline = models.IntegerField(db_column='STARTLINE')  # Field name made lowercase.
    endline = models.IntegerField(db_column='ENDLINE')  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    normalized_size = models.IntegerField(db_column='NORMALIZED_SIZE', blank=True, null=True)  # Field name made lowercase.
    project = models.CharField(db_column='PROJECT', max_length=400, blank=True, null=True)  # Field name made lowercase.
    tokens = models.IntegerField(db_column='TOKENS', blank=True, null=True)  # Field name made lowercase.
    internal = models.IntegerField(db_column='INTERNAL')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'FUNCTIONS'

    def __str__(self):
        return "{type},{name},{st_line},{end_line},{tokens}".format(type=self.type,
                                                                 name=self.name,
                                                                 st_line=self.startline,
                                                                 end_line=self.endline,
                                                                    tokens=self.tokens)
