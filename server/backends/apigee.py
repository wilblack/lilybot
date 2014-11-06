"""
A backend to connect to ApiGee


Usage:

api = ApiGeeClient()
sensor_values = {"timestamp": "2014-11-05T23:52:07Z", "message": {"command": "sensor_values", "kwargs": {"temp": 24.9, "bot_package": "grovebot", "humidity": 62.1, "light": 447, "touch": 0, "pir": 0}}, "from": "monitor.solalla.ardyh", "bot_name": "rpi3.solalla.ardyh"}
api.post('sensor_values', sensor_values)


https://api.usergrid.com/wilblack/sandbox/sensor_values?access_token=YWMtFQOvnGVBEeSybiMsBDBtogAAAUmmRresAXzSPcMeMhi-IroLVeqlNoexalA
"""
import requests, json

APIGEE_USERNAME = "wilblack"
APIGEE_TOKEN = "YWMtFQOvnGVBEeSybiMsBDBtogAAAUmmRresAXzSPcMeMhi-IroLVeqlNoexalA"
APIGEE_BASE_URI = "https://api.usergrid.com/%s/sandbox/" %(APIGEE_USERNAME)


class ApiClientBase(object):
    """
    A class to help build formstacks
    """

    def __init__(self):
        self.bad_responses = []

    def get(self, resource, data):
        uri = "%s%s" %(self.base_uri, resource)
        
        resp = requests.get(uri)
        content = json.loads(resp.text)
        
        if resp.status_code >= 300: 
            print res.text
            self.bad_responses.append(resp)
        return resp


    def post(self, resource, data):
        uri = "%s%s?access_token=%s" %(self.base_uri, resource, self.token)

        data = json.dumps(data)
        resp = requests.post(uri, data=data)
        content = json.loads(resp.text)
        
        if resp.status_code >= 300: 
            print "ERROR: %s" % (resp.status_code)
            print resp.text
            self.bad_responses.append(resp)
        return resp



    def update(self, resource, data):
        pass

    def print_errors(self):
        print "******** ERRROR REPORT ************"
        for res in self.bad_responses:
            print resp



class ApiGeeClient(ApiClientBase):

    def __init__(self):
        self.usename = APIGEE_USERNAME
        self.token = APIGEE_TOKEN
        self.base_uri = APIGEE_BASE_URI

        super(ApiGeeClient, self).__init__()




