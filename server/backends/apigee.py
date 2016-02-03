"""
A backend to connect to ApiGee


Usage:

api = ApiGeeClient()
sensor_values = {"timestamp": "2014-11-05T23:52:07Z", "message": {"command": "sensor_values", "kwargs": {"temp": 24.9, "bot_package": "grovebot", "humidity": 62.1, "light": 447, "touch": 0, "pir": 0}}, "from": "monitor.solalla.ardyh", "bot_name": "rpi3.solalla.ardyh"}
api.post('sensor_values', sensor_values)


https://api.usergrid.com/wilblack/sandbox/sensor_values?access_token=YWMtFQOvnGVBEeSybiMsBDBtogAAAUmmRresAXzSPcMeMhi-IroLVeqlNoexalA
"""
import requests, json

from backends import ApiClientBase

APIGEE_USERNAME = "wilblack"
APIGEE_TOKEN = "YWMtFQOvnGVBEeSybiMsBDBtogAAAUmmRresAXzSPcMeMhi-IroLVeqlNoexalA"

APIGEE_CLIENT_ID = "YXA6URl94E0TEeSCwuPO0mAKgw"
APIGEE_CLIENT_SECRECT = "YXA6wd-UdXgImKXHBRk-6ZyTzT46UwM"

#APIGEE_TOKEN = "YXA6wd-UdXgImKXHBRk-6ZyTzT46UwM"
APIGEE_BASE_URI = "https://api.usergrid.com/%s/sandbox/" %(APIGEE_USERNAME)





class ApiGeeClient(ApiClientBase):

    def __init__(self):
        self.usename = APIGEE_USERNAME
        self.token = APIGEE_TOKEN
        self.base_uri = APIGEE_BASE_URI

        super(ApiGeeClient, self).__init__()

    def reset_access_token(self):
        uri = "%s%s" %(self.base_uri, 'token')
        data = {
            'grant_type':'client_credentials',
            'client_id': APIGEE_CLIENT_ID,
            'client_secret': APIGEE_CLIENT_SECRECT
        }
        resp = requests.post(uri, data=data)
        
        content = json.loads(resp.text)
        self.token = content['access_token']
        print self.token
        return self.token


