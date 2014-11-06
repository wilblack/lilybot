from django.contrib.auth.models import User 
from pforms.models import FormStack, Question, Block, Form

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class Api(object):
    """
    A class to help build formstacks
    """

    def __init__(self):
        token = Token.objects.get(user__username='p97dev')
        self.client = APIClient()
        print "Token: %s" %(token)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # self.client.force_authenticate(user=user)
        self.bad_responses = []

    def get(self, resource, data):
        print "\nGET url: %s" %(resource)
        print "data: %s" %(data)
        res = self.client.get(resource, data, format='json')
        print "status code: ", res.status_code
        if res.status_code >= 300: 
            print res.content
            res.request_data = data
            self.bad_responses.append(res)
        return res


    def post(self, resource, data):
        print "\nPOST url: %s" %(resource)
        print "data: %s" %(data)
        res = self.client.post(resource, data, format='json')
        if res.status_code >= 300:
            print "status code: ", res.status_code
            print res.content
            res.request_data = data
            self.bad_responses.append(res)
        return res

    def update(self, resource, data):
        """
        A partial update using PATCH
        """
        print "\nPATCH url: %s" %(resource)
        print "data: %s" %(data)
        res = self.client.patch(resource, data, format='json')
        print "status code: ", res.status_code
        if res.status_code >= 300:
            print res.content
            return res
            self.bad_responses.append(res)

    def print_errors(self):
        print "******** ERRROR REPORT ************"
        for res in self.bad_responses:
            print "%s -%s %s" % (res.status_code, res.request['REQUEST_METHOD'], res.request['PATH_INFO'])
            print res.data
            print "REQUEST_DATA", res.request_data
