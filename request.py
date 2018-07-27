import requests
import json

class get_request():

    def get_json_from_request(self, request_url):
        response = requests.get(request_url)
        responseStatus = response.status_code
        if responseStatus == 200:
            return json.loads(response.text)
        else:
            print('No response from the requested url')
            return responseStatus