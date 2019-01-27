# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class BCBClones(models.Model):
    use_db = 'bcb'

    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    function_id_one = models.BigIntegerField(db_column='FUNCTION_ID_ONE')  # Field name made lowercase.
    function_id_two = models.BigIntegerField(db_column='FUNCTION_ID_TWO')  # Field name made lowercase.
    functionality_id = models.BigIntegerField(db_column='FUNCTIONALITY_ID')  # Field name made lowercase.
    type = models.TextField(db_column='TYPE')  # Field name made lowercase.
    syntactic_type = models.IntegerField(db_column='SYNTACTIC_TYPE')  # Field name made lowercase.
    similarity_line = models.FloatField(db_column='SIMILARITY_LINE')  # Field name made lowercase.
    similarity_token = models.FloatField(db_column='SIMILARITY_TOKEN')  # Field name made lowercase.
    min_size = models.IntegerField(db_column='MIN_SIZE')  # Field name made lowercase.
    max_size = models.IntegerField(db_column='MAX_SIZE')  # Field name made lowercase.
    min_pretty_size = models.IntegerField(db_column='MIN_PRETTY_SIZE')  # Field name made lowercase.
    max_pretty_size = models.IntegerField(db_column='MAX_PRETTY_SIZE')  # Field name made lowercase.
    min_judges = models.IntegerField(db_column='MIN_JUDGES')  # Field name made lowercase.
    min_confidence = models.IntegerField(db_column='MIN_CONFIDENCE')  # Field name made lowercase.
    min_tokens = models.IntegerField(db_column='MIN_TOKENS')  # Field name made lowercase.
    max_tokens = models.IntegerField(db_column='MAX_TOKENS')  # Field name made lowercase.
    internal = models.IntegerField(db_column='INTERNAL')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CLONES'
        #unique_together = (('function_id_one', 'function_id_two'),)


    #def get_id(self, file, startline, endline, folder):
    #    return None

    #def is_clone(self, file1, startline1, endline1, folder1, file2, startline2, endline2, folder2):
    #    id1 = self.get_id(file1, startline1, endline1, folder1)
    #    id2 = self.get_id(file2, startline2, endline2, folder2)
    #    res = self.is_clone(id1, id2)
    #    return True