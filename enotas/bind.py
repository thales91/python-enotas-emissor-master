import urllib
from .authorization import AuthorizationRequest
import re
from .json_import import simplejson
import hmac
from hashlib import sha256
import six
from six.moves.urllib.parse import quote
import sys

re_path_template = re.compile('{\w+}')


def encode_string(value):
    return value.encode('utf-8') \
        if isinstance(value, six.text_type) else str(value)


class ENotasClientError(Exception):
    def __init__(self, error_message, status_code=None):
        self.status_code = status_code
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return "(%s) %s" % (self.status_code, self.error_message)
        else:
            return self.error_message


class ENotasAPIError(Exception):

    def __init__(self, status_code, error_type, error_message, *args, **kwargs):
        self.status_code = status_code
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self):
        return "(%s) %s-%s" % (self.status_code, self.error_type, self.error_message)


def bind_method(**config):

    class ENotasAPIMethod(object):

        path = config['path']
        method = config.get('method', 'GET')
        accepts_parameters = config.get("accepts_parameters", [])
        signature = config.get("signature", False)
        requires_target_user = config.get('requires_target_user', False)
        paginates = config.get('paginates', False)
        root_class = config.get('root_class', None)
        response_type = config.get("response_type", "list")
        include_secret = config.get("include_secret", False)
        objectify_response = config.get("objectify_response", True)
        exclude_format = config.get('exclude_format', True)

        def __init__(self, api, *args, **kwargs):
            self.api = api
            self.return_json = kwargs.pop("return_json", False)
            self.parameters = {}
            self._build_parameters(args, kwargs)
            self._build_path()

        def _build_parameters(self, args, kwargs):
            # via tweepy https://github.com/joshthecoder/tweepy/
            for index, value in enumerate(args):
                if value is None:
                    continue

                try:
                    self.parameters[accepts_parameters[index]] = encode_string(value)
                except IndexError:
                    raise ENotasClientError("Too many arguments supplied")

            for key, value in six.iteritems(kwargs):
                if value is None:
                    continue
                if key in self.parameters:
                    raise ENotasClientError("Parameter %s already supplied" % key)
                self.parameters[key] = encode_string(value)
            
        def _build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                try:
                    value = quote(self.parameters[name])
                except KeyError:
                    raise Exception('No parameter value found for path variable: %s' % name)
                del self.parameters[name]

                self.path = self.path.replace(variable, value)

            if self.api.format and not self.exclude_format:
                self.path = self.path + '.%s' % self.api.format

        def _build_pagination_info(self, content_obj):
            """Extract pagination information in the desired format."""
            if self.response_type == "list":
                pageNumber = int(self.parameters.get('pageNumber')) + 1
                pageSize = int(self.parameters.get('pageSize'))
                pagination = content_obj.get('totalRecords', {})
                if pageNumber * pageSize  < int(pagination):
                    return pageNumber, pagination
                else:
                    return pageNumber - 1, pagination
            else:
                return 0, 0
            
        def _do_api_request(self, url, method="GET", body=None, headers=None):
            
            headers = headers or {}

            response, content = AuthorizationRequest(self.api).make_request(url, method=method, body=body, headers=headers)
            print content
            if response['status'] == '503' or response['status'] == '429':
                raise ENotasAPIError(response['status'], "Rate limited", "Your client is making too many request per second")
            try:
                content_obj = simplejson.loads(content)
            except ValueError:
                raise ENotasClientError('Unable to parse response, not valid JSON.', status_code=response['status'])
            # Handle OAuthRateLimitExceeded from Instagram's Nginx which uses different format to documented api responses
           
            api_responses = []
            status_code = response['status']
            if status_code == '200':
                if not self.objectify_response:
                    return content_obj, None

                if self.response_type == 'list':
                    for entry in content_obj['data']:
                        if self.return_json:
                            api_responses.append(entry)
                        else:
                            obj = self.root_class.object_from_dictionary(entry)
                            api_responses.append(obj)
                elif self.response_type == 'entry':
                    data = content_obj
                    if self.return_json:
                        api_responses = data
                    else:
                        api_responses = self.root_class.object_from_dictionary(data)
                elif self.response_type == 'empty':
                    pass
                next_ , total = self._build_pagination_info(content_obj)
                return api_responses, next_, total 
            else:
                raise ENotasAPIError(status_code, content_obj['meta']['error_type'], content_obj['meta']['error_message'])

        def _paginator_with_url(self, url, method="GET", body=None, headers=None):
            headers = headers or {}
            pages_read = 0
            while url and (self.max_pages is None or pages_read < self.max_pages):
                api_responses, url = self._do_api_request(url, method, body, headers)
                pages_read += 1
                yield api_responses, url
            return

        
        def execute(self):
            url, method, body, headers = AuthorizationRequest(self.api).prepare_request(self.method,
                                                                                 self.path,
                                                                                 self.parameters,
                                                                                 include_secret=self.include_secret)

        
            content, next, total = self._do_api_request(url, method, body, headers)
            if self.paginates:
                return content, next, total
            else:
                return content

    def _call(api, *args, **kwargs):
        method = ENotasAPIMethod(api, *args, **kwargs)
        return method.execute()

    return _call
