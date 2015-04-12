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
        return content


    def post(self, resource, data):
        uri = "%s%s?access_token=%s" %(self.base_uri, resource, self.token)

        resp = requests.post(uri, data=json.dumps(data))
        content = json.loads(resp.text)
        
        if resp.status_code >= 300: 
            print "ERROR: %s" % (resp.status_code)
            print resp.text
            self.bad_responses.append(resp)
            
            if (content['error'] == 'expired_token'):
                self.reset_access_token()
                self.post(resource, data)

        return content



    def update(self, resource, data):
        pass

    def print_errors(self):
        print "******** ERRROR REPORT ************"
        for res in self.bad_responses:
            print resp
