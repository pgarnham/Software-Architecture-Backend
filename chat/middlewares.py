import requests
class IPGetter:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4').text
        response = self.get_response(request)
        response['ip-header'] = ip
        return response
