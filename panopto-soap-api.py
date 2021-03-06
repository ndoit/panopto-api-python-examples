# This example shows how to create a SOAP client using Panopto's wsdl files and the pysimplesoap library in Python.
# It also shows how to construct an object to use as an argument in these calls, and provides examples of calling
# both the CreateUser and AddMembersToInternalGroup methods from the API.

import hashlib
from datetime import datetime
from dateutil import tz
# from datetime import timezone, datetime
import configparser
# import uuid
import logging
# https://github.com/suds-community/suds
from suds.client import Client


'''
    configure logging
'''
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)


def generateauthcode(userkey, servername, sharedSecret):
    '''
        function used to create auth code for SOAP requests
        'userkey' is either user's Panopto admin's username, or the username decorated with the the external provider's instance name if it is an external admin user.
        'servername' is the domain name of the Panopto server to make the SOAP request to (e.g. demo.hosted.panopto.com)
        'sharedSecret' is the Application key from the provider on the Panopto Identity Provider's page.
    '''
    payload = userkey + '@' + servername
    signedPayload = payload + '|' + sharedSecret
    m = hashlib.sha1()
    m.update(signedPayload.encode('utf-8'))
    authcode = m.hexdigest().upper()
    return authcode


# '''
# Create a new public ID for the user to be created.
# '''
# studentUserID = uuid.uuid1()
#
# '''
# Create a user object with information for the new user. Parameters here must be in this order to be accepted by the server
# '''
# studentUser = {'Email': "test@test.com",
#                'EmailSessionNotifications': "true",
#                'FirstName': "Student",
#                # Optional list of GUIDs as strings of the groups that the user should be a member in.
#                'GroupMemberships': ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"],
#                'LastName': "User",
#                # User's role on Panotpo. "None" will grant the user the sitewide 'Viewer' role.
#                'SystemRole': "None",
#                # Optional description of user.
#                'UserBio': "",
#                'UserId': str(studentUserID),
#                # Panopto login ID for student. May be anything.
#                'UserKey': "studentuser",
#                # Optional custom URL for user's settings.
#                'UserSettingsUrl': ""
#                }

'''
Admin auth info for making SOAP calls
'''
secrets_config = configparser.ConfigParser()
secrets_config.read('connectioninfo.conf')
# username of admin user in Panopto.
userkey = secrets_config['Common']['user']
# password of admin user on Panopto server. Only required if external provider does not have a bounce page.
password = secrets_config['Common']['password']
# Instance name of external provider on Panotpo
providername = secrets_config['Common']['idp_provider']
# Application key from provider on Panotpo
applicationkey = secrets_config['Common']['application_key']
# Name of the panopto server to add the user to.
servername = secrets_config['Common']['server_address']


'''
Create a SOAP client object using the
'''
url = "https://" + servername + "/Panopto/PublicAPI/4.6/UsageReporting.svc?wsdl"
client = Client(url)
'''
Generate auth code for making SOAP call using admin user info.
'''
authcode = generateauthcode(userkey, servername, applicationkey)

'''
 Create AuthenticationInfo object to be passed to server with SOAP call
'''
AuthenticationInfo = {'AuthCode': authcode, 'Password': password, 'UserKey': userkey}

sakai_courses_folder_id = '1cacbfae-dd5b-43ac-90a1-7d93ef3410a0'

# {'action': 'ExportFolderAnalytics',
#            'folder': 'c6d51db2-b319-44ae-a190-2c5b06e926be',
#            'startTime': '2020-06-01T00%3A00%3A00-04%3A00',
#            'endTime': '2020-07-07T23%3A59%3A59-04%3A00',
#            'type': 'ViewsAndDownloads',
#            'timezone': 'America%2FIndianapolis'}


begindate = datetime(2020, 6, 1).astimezone(tz.UTC)
enddate = datetime(2020, 7, 1).astimezone(tz.UTC)

'''
    get system usage summary
'''
result = client.service.GetSystemSummaryUsage(
    auth=AuthenticationInfo,
    beginRange=begindate,
    endRange=enddate,
    granularity='Daily'
)

print(result)

# getusageresponse = client.GetFolderSummaryUsage(
#     auth=AuthenticationInfo,
#     folderId=sakai_courses_folder_id,
#     beginRange=begindate,
#     endRange=enddate,
#     granularity='Daily'
# )
# breakpoint()
# print(getusageresponse)

# getuser = client.GetUserByKey(
#     auth=AuthenticationInfo,
#     userKey='panopto_analytics'
# )
#
# print(getuser)

# '''
# Soap call to create user in panopto. Result will contain user's public ID if successful.
# '''
# createUserResponse = client.CreateUser(
#     auth=AuthenticationInfo,
#     user=studentUser,
#     # Initial password for created user. This may be reset manually.
#     initialPassword="studentpassword"
# )
# Show response from attempt to create user.
# print(createUserResponse)

# '''
# Soap call to add a user to an internal group in Panopto.
# This will give them the permissions inherited by members
# of the group on associated folders and sessions.
# '''
# addMembersToGroupResponse = client.AddMembersToInternalGroup(
#     auth=AuthenticationInfo,
#     # public GUID of group to add members to
#     groupId="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
#     # Initial password for created user. This may be reset manually.
#     memberIDs=["yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy", "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"]
# )

# Show response from attempt to add members to group.
# print(addMembersToGroupResponse)
