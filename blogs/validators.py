from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def image_size(value):
    limit = 2 * 1024 * 1024
    if value.size > limit :
        raise ValidationError( 'Image Size too large Maximum of 5mb Allowed')