from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client.file import Storage
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-ken-sears-eval.json
SCOPES = "https://www.googleapis.com/auth/gmail.modify"
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Skills Evaluation for BYU OIT'

class Gmail(object):
    """Class to provide methods needed to send email through gmail account via the Gmail API"""
    def __init__(self):
        self.credentials = None

    def getCredentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        #home_dir = os.path.expanduser('~')
        credential_dir = "./credentials"
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, "gmail-ken-sears-eval.json")

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
        return credentials

    def sendMail(self, message):
        """Sends an email through the Gmail API.

        Creates a Gmail API service object and sends an email based on the message passed in.

        Args:
            message: A base64url encoded email object

        Returns:
            The email message
        """
        if not self.credentials:
            self.credentials = self.getCredentials()

        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build("gmail", "v1", http=http)

        try:
            email_message = (service.users().messages().send(userId="me", body=message).execute())
            return email_message
        except errors.HttpError, error:
            print("An error occurred: %s" % error)
