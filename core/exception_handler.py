from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.

    if response:
        if hasattr(exc, 'default_detail_code'):
            response.data['detail_code'] = exc.default_detail_code
        elif hasattr(exc, 'detail_code'):
            response.data['detail_code'] = exc.detail_code

    return response
