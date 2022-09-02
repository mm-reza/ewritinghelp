from django.core.exceptions import ValidationError
from django import forms


def validate_file_size(value):
    filesize= value.size
    limit_mb = 2
    if filesize > limit_mb * 1024 * 1024:
        raise forms.ValidationError("The maximum file size that can be uploaded is 2MB / Max size of file is %s MB" % limit_mb)
    else:
        return value