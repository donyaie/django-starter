from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList
from collections import OrderedDict


class DataStatusMessage_Renderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):

        status_code = renderer_context['response'].status_code
        response = dict()

        if str(status_code).startswith('2'):
            # response['detail'] = data.pop('detail') if 'detail' in data.keys() else None

            # # if 'detail' in data.keys():
            # #     response['detail'] = data.pop('detail')
            # if data != None and  type(data) == dict  and  'results' in data.keys():
            #     results_sign = data.get('results', {})
            # else:
            #

            # if(type(data) == OrderedDict):
            if (data == None):
                data = dict()

            if type(data) != ReturnList:
                results_sign = data.get('results', {})
            else:
                results_sign = dict()

            if type(results_sign) == ReturnList:
                response['results'] = data['results']
                response['count'] = data['count']
                response['next'] = data['next']
                response['previous'] = data['previous']
            else:
                response['results'] = data

        elif str(status_code).startswith('4'):

            response = data

        elif str(status_code).startswith('5'):
            response['detail'] = "Server Error"
            response['results'] = dict()

        else:
            response['detail'] = "Message do not handle correctly."
            response['results'] = data

        return super(DataStatusMessage_Renderer, self).render(response, accepted_media_type, renderer_context)
