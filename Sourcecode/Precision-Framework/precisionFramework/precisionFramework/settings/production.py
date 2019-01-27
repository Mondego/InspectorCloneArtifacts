# -*- coding: utf-8 -*-
from .base import *
DEBUG = False
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
DATASET_ROOT = os.path.join(BASE_DIR, "dataset/")
DOWNLOADS_ROOT = os.path.join(BASE_DIR, "downloads/")
ALLOWED_HOSTS = ["www.inspectorclone.org","inspectorclone.org"]
FILE_UPLOAD_PERMISSIONS = 0o775