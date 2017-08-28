"""This module does..."""
import httplib
import base64
import json
import config

class GitHub(object):
    """This class provides the methods needed to get the needed information from GitHub"""
    def __init__(self):
        auth = base64.b64encode("%s:%s" % (config.GITHUB['username'], config.GITHUB['password']))
        self.header = {"User-Agent": config.GITHUB['username'], "Authorization": "Basic %s" % auth}
        self.gitHubConn = httplib.HTTPSConnection('api.github.com', 443)

    def getOrgMembers(self, orgName):
        """Gets the members of an organization
        
        Args: 
            orgName: The GitHub name of the organization

        Returns:
            A python list of dictionaries for each organization members
        """
        self.gitHubConn.request('GET', "/orgs/%s/members" % orgName, None, self.header)
        response = self.gitHubConn.getresponse()
        orgMembers = json.loads(response.read())
        return orgMembers

    def getUser(self, loginName):
        """Gets a GitHub user
        
        Args: 
            loginName: The GitHub login name of the user

        Returns:
            A python dictionary with user information
        """
        self.gitHubConn.request('GET', "/users/%s" % loginName, None, self.header)
        response = self.gitHubConn.getresponse()
        user = json.loads(response.read())
        return user
