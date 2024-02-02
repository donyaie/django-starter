from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotAcceptable


class InvalidActivationCodeException(NotAcceptable):
    default_detail = _('Activation code is wrong')
    default_detail_code = 'invalid_activation_code'
