import sys
sys.path.insert(0, './lib')
import base64
from email.mime.text import MIMEText
import json
from github import GitHub
from gmail import Gmail
import boto
from boto.s3.key import Key
import config

def createMessage(sendTo):
    """Create a message for an email.

    Args:
        sendTo: Email address of the receiver.

    Returns:
        An object containing a base64url encoded email object.
    """
    messageBody = "Nameless Member,\n\n"
    messageBody += "We don't know what to call you. "
    messageBody += "Please go to the link provided and take a moment to update your GitHub profile to include your name.\n\n"
    messageBody += "https://github.com/settings/profile\n\n"
    messageBody += "Thank You,\n"
    messageBody += "Your friendly administrator"
    message = MIMEText(messageBody)
    message['to'] = sendTo
    message['from'] = config.GMAIL['from_address']
    message['subject'] = "Nameless %s member" % config.GITHUB['organization']
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def uploadNamelessToS3(fileContents):
    """Upload file contents to AWS S3

    Args:
        fileContents: formatted string of data to upload to S3

    Returns:
        Nothing
    """
    s3_connection = boto.connect_s3(config.AWS['aws_access_key_id'], config.AWS['aws_secret_access_key'])
    bucket = s3_connection.get_bucket(config.AWS['s3_bucket'])
    key = Key(bucket)
    key.key = config.AWS['s3_bucket_key']
    key.content_type = "application/json"
    key.set_contents_from_string(fileContents)

def main():
    # Get all members of the organization and add them to
    # namelessMembers if they don't have a name
    print "Gathering nameless members..."
    namelessMembers = []
    github = GitHub()
    members = github.getOrgMembers(config.GITHUB['organization'])
    for member in members:
        memberProfile = github.getUser(member['login'])
        if not memberProfile['name']:
            namelessMembers.append(memberProfile)
    
    # Print contents of namelessMembers to the terminal
    print json.dumps(namelessMembers, indent=4)
    
    # loop through namelessMembers and send them an email through
    # an authenticated gmail account.
    print "Emailing nameless members..."
    gmail = Gmail()
    for nameless in namelessMembers:
        # Check to see if email is public.
        # If it's not public, I can't see any other way to send them an email.
        if nameless['email']:
            gmail.sendMail(createMessage(nameless['email']))
            print "%s: %s" % (nameless['login'], nameless['email'])
        else:
            print "%s: No Email" % nameless['login']

    # upload nameless list to s3
    print "Uploading nameless member info to s3..."
    uploadNamelessToS3(json.dumps(namelessMembers, indent=4))
    print "done"

if __name__ == '__main__':
    main()
