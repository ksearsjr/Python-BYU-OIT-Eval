# Python Skills Evaluation for BYU OIT Software Developer - AWS Position (Job ID 64987)

### Setup
You should only need to have Python 2.7.x installed. I ran it with 2.7.10.

No additional libraries are required to be installed to run this code. I used other libraries but they should all be included with my code in the lib folder.

In order for the app to work, you should only need to put the required information in the config.py file. All information in that file is required.

When you first run the code, if it's required to send an email, it will ask you to authenticate with your own Gmail account. It will then use your account to send the email through the Gmail API.

### How to run the app
Inside the directory where the code resides run this in a terminal:
`python notify_nameless.py`

### Assumptions
This was developed on my Mac where I used the native installation of Python version 2.7.10. I have not tested this on any other OS. Please let me know if you have trouble running it.

I'm assuming this won't actually be ran remotely on a server. The Gmail API would need to be implemented slightly different if that were the case.

In order to send an email to an organization member, the member must have the public email field set inside the profile page. I couldn't figure out any other way to get the users email through the API.

