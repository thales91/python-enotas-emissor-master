from .json_import import simplejson
import json
from six.moves.urllib.parse import urlencode
from httplib2 import Http
from hashlib import sha256
import mimetypes
import six
import hmac


class AuthorizationExchangeError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description


class Authorization(object):
    host = None
    base_path = None
    protocol = "http"
    # override with 'ENotas', etc
    api_name = "Generic API"

    def __init__(self, api_key=None):
        self.api_key = api_key

class AuthorizationRequest(object):
    def __init__(self, api):
        self.api = api

    def _generate_sig(self, endpoint, params, secret):
        sig = endpoint
        for key in sorted(params.keys()):
            sig += '|%s=%s' % (key, params[key])
        return hmac.new(secret.encode(), sig.encode(), sha256).hexdigest()

    def url_for_get(self, path, parameters):
        return self._full_url_with_params(path, parameters)

    def get_request(self, path, **kwargs):
        return self.make_request(self.prepare_request("GET", path, kwargs))

    def post_request(self, path, **kwargs):
        return self.make_request(self.prepare_request("POST", path, kwargs))

    def _full_url(self, path, include_secret=False, include_signed_request=True):
        return "%s://%s%s%s" % (self.api.protocol,
                                  self.api.host,
                                  self.api.base_path,
                                  path)

    def _full_url_with_params(self, path, params, include_secret=False, include_signed_request=True):
        return (self._full_url(path, include_secret) +"?"+ 
                self._full_query_with_params(params))

    def _full_query_with_params(self, params):
        params = (urlencode(params)) if params else ""
        return params
   
    def _post_body(self, params):
        js = json.dumps(params["data"])
        print js
        return json.loads(js)

    def _encode_multipart(self, params, files):
        boundary = "MuL7Ip4rt80uND4rYF0o"

        def get_content_type(file_name):
            return mimetypes.guess_type(file_name)[0] or "application/octet-stream"

        def encode_field(field_name):
            return ("--" + boundary,
                    'Content-Disposition: form-data; name="%s"' % (field_name),
                    "", str(params[field_name]))

        def encode_file(field_name):
            file_name, file_handle = files[field_name]
            return ("--" + boundary,
                    'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, file_name),
                    "Content-Type: " + get_content_type(file_name),
                    "", file_handle.read())

        lines = []
        for field in params:
            lines.extend(encode_field(field))
        for field in files:
            lines.extend(encode_file(field))
        lines.extend(("--%s--" % (boundary), ""))
        body = "\r\n".join(lines)

        headers = {"Content-Type": "multipart/form-data; boundary=" + boundary,
                   "Content-Length": str(len(body))}

        return body, headers

    def prepare_and_make_request(self, method, path, params, include_secret=False):
        url, method, body, headers = self.prepare_request(method, path, params, include_secret)
        return self.make_request(url, method, body, headers)

    def prepare_request(self, method, path, params, include_secret=False):
        url = body = None
        headers = {}

        if not params.get('files'):
            if method == "POST":
                body = self._post_body(params)
                print body
                headers = {'content-type': 'application/json; charset=utf-8', "Authorization": 'basic '+ self.api.api_key, 'Accept': 'application/json'}
                url = self._full_url(path, include_secret)

            else:
                apiBasic = 'basic ' + self.api.api_key
                headers = {"Authorization": apiBasic, 'Accept': 'application/json'}
                url = self._full_url_with_params(path, params, include_secret)
        else:
            body, headers = self._encode_multipart(params, params['files'])
            url = self._full_url(path)
        return url, method, body, headers

    def make_request(self, url, method="GET", body=None, headers=None):
        headers = headers or {}
        if not 'User-Agent' in headers:
            headers.update({"User-Agent": "%s Python Client" % self.api.api_name})
        # https://github.com/jcgregorio/httplib2/issues/173
        # bug in httplib2 w/ Python 3 and disable_ssl_certificate_validation=True
        http_obj = Http() #if six.PY3 else Http(disable_ssl_certificate_validation=True)        
        return http_obj.request(url, method, body=body, headers=headers)
