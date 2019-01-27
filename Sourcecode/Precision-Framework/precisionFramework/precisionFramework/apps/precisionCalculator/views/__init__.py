from django.http import HttpResponse

from .tool import *
from .experiment import *
from .experimentaction import *
from .experimentdetail import *
from .judge import *
import os
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str


def download_files(request, filename):
    if filename == "dataset":
        downloads_root = getattr(settings, "DOWNLOADS_ROOT", None)
        file_path = "{root}/{filename}".format(root=downloads_root,
                                               filename="dataset_java_source.zip")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    elif filename == "demopairs":
        downloads_root = getattr(settings, "DOWNLOADS_ROOT", None)
        file_path = "{root}/{filename}".format(root=downloads_root,
                                               filename="demo_clonepairs.zip")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
    elif filename == "oreo":
        downloads_root = getattr(settings, "DOWNLOADS_ROOT", None)
        file_path = "{root}/{filename}".format(root=downloads_root,
                                               filename="oreo.pdf")
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response

    raise Http404
