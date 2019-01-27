# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from .. import managers
import re
import hashlib

# Create your models here.

class Block(models.Model):
    folder_name = models.CharField(max_length=500)
    file_name = models.CharField(max_length=500)
    start_line = models.IntegerField()
    end_line = models.IntegerField()
    bcb_function_id = models.IntegerField(default=-999, unique=True)
    tokens = models.IntegerField()
    normalized_size = models.IntegerField()
    hash = models.CharField(max_length=64)
    pattern_inline_comments = "//.*(\\n|\\r|\\r\\n)"
    pattern_block_comments = "/\\*.*\\*/"
    pattern_new_lines = "\\n|\\r|\\r\\n"
    pattern_whitespace = "\s+"

    class Meta:

        verbose_name = _("Block")
        verbose_name_plural = _("Blocks")
        ordering = ("folder_name", "file_name", "start_line", "end_line")

    def __str__(self):
        return "{folder},{filename},{st_line},{end_line}".format(folder=self.folder_name,
                                                                 filename=self.file_name,
                                                                 st_line=self.start_line,
                                                                 end_line=self.end_line)


    def getSourceCode(self):
        dataset_root = getattr(settings, "DATASET_ROOT", None)
        if dataset_root:
            file_path = "{root}/{folder}/{filename}".format(root=dataset_root,
                                                       folder=self.folder_name,
                                                       filename = self.file_name)
            count = min(1,self.start_line)
            code_lines = ""
            with open(file_path,encoding="utf-8", mode="r") as f:
                for line in f:
                    if count >self.end_line:
                        return code_lines
                    if count >=self.start_line:
                        code_lines = code_lines + line
                    count +=1
            if self.end_line > count:
                raise SystemError("Error with block" + str(self))
            return code_lines
        else:
            raise SystemError("DATASET_ROOT not set.")

    def getFlatString(self, input):
        result = re.sub(pattern=Block.pattern_inline_comments, repl="", string=input)
        result = re.sub(pattern=Block.pattern_new_lines, repl="", string=result)
        result = re.sub(pattern=Block.pattern_block_comments, repl="", string=result)
        result = re.sub(pattern=Block.pattern_whitespace, repl="", string=result)
        return result

    def getSourceCodeHash(self):
        code_lines = self.getSourceCode()
        flat_line = self.getFlatString(code_lines)
        return self.getHash(flat_line)


    def getHash(self, input):
        m = hashlib.sha256()
        m.update(input.encode(encoding="utf-8"))
        return m.hexdigest()
