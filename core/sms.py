import os

# from twilio.rest import Client
from django.conf import settings

# account_sid = settings.TWILIO_ACCOUNT_SID
# auth_token = settings.TWILIO_ACCOUNT_AUTH
# verification_service = settings.TWILIO_VERIFICATION_SERVICE

# client = Client(account_sid, auth_token)


def send_verification_sms(phone_number):
    pass
    # try:
    #     # client.verify \
    #     #     .services(verification_service) \
    #     #     .verifications \
    #     #     .create(to=phone_number, channel='sms')
    #     pass
    # except Exception as e:
    #     pass


def check_verification(phone_number, code):
    return True
    # try:
    #     pass
    #     # verification_check = client.verify \
    #     #     .services(verification_service) \
    #     #     .verification_checks \
    #     #     .create(to=phone_number, code=code)
    #     # return verification_check.status == "approved"
    # except Exception as e:
    #     pass
