from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class TagSlugValidator(RegexValidator):
    regex = r'^[-a-zA-Z0-9_]+$'
    message = _('Invalid Tag Slug')
