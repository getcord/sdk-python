import datetime
import json
import jwt
import requests

CORD_ENDPOINT = "https://api.cord.com/v1/"

from enum import Enum

class status(Enum):
    ACTIVE = "active"
    DELETED = "deleted"

class platformUserVariables:
    def __init__(self, email: str, name: str = None, status: status = None, profile_picture_url: str = None, first_name: str = None, last_name: str = None):
        self.email = email
        self.name = name
        self.status = status
        self.profile_picture_url = profile_picture_url
        self.first_name = first_name
        self.last_name = last_name

class platformOrganizationVariables:
    def __init__(self, name: str, status: status = None, members: list[str] = None):
        self.name = name
        self.status = status
        self.members = members

class clientPlatformUserVariables:
    def __init__(self, id: str, email: str, name: str = None, status: status = None, profile_picture_url: str = None, first_name: str = None, last_name: str = None):
        self.id = id
        self.email = email
        self.name = name
        self.status = status
        self.profile_picture_url = profile_picture_url
        self.first_name = first_name
        self.last_name = last_name

class clientPlatformOrganizationVariables:
    def __init__(self, id: str, name: str, status: status = None, members: list[str] = None):
        self.id = id
        self.name = name
        self.status = status
        self.members = members

def toJson(obj):
    return json.dumps(obj, default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value),
                      indent=4,
                      allow_nan=False)

def get_client_auth_token(app_id: str, secret: str, payload: json):
    return jwt.encode(
        payload = { 
            "app_id": app_id, 
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=1), 
            "iat": datetime.datetime.now(),
            **payload 
        },
        key = secret,
        algorithm='HS512'
    )

def get_server_auth_token(app_id: str, secret: str):
    return jwt.encode(
        payload = { 
            "app_id": app_id, 
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=1),
            "iat": datetime.datetime.now()
        },
        key = secret,
        algorithm='HS512'
    )

class CordClient:
    def __init__(self, app_id, secret):
        self.app_id = app_id
        self.secret = secret


    def sync_cord_user(self, user: clientPlatformUserVariables):
        auth_token: str = get_server_auth_token(self.app_id, self.secret)
        userId = user.id
        delattr(user, "id")

        headers = {
            "Authorization": "Bearer {}".format(auth_token),
            "Content-Type": "application/json"
        }
        response = requests.put(CORD_ENDPOINT + "users/" + userId, headers=headers, data=toJson(user))

        return response.json()

    def sync_cord_organization(self, organization: clientPlatformOrganizationVariables):
        auth_token: str = get_server_auth_token(self.app_id, self.secret)
        orgId = organization.id
        delattr(organization, "id")

        headers = {
            "Authorization": "Bearer {}".format(auth_token),
            "Content-Type": "application/json"
        }
        response = requests.put(CORD_ENDPOINT + "organizations/" + orgId, headers=headers, data=toJson(organization))

        return response.json()

    def batch_sync_cord_users_and_organizations(self, users: list[clientPlatformUserVariables], organizations: list[platformOrganizationVariables]):
        auth_token: str = get_server_auth_token(self.app_id, self.secret)

        headers = {
            "Authorization": "Bearer {}".format(auth_token),
            "Content-Type": "application/json"
        }
        request_body = "{{ \"organizations\": {}, \"users\": {} }}".format(toJson(organizations), toJson(users))
        response = requests.post(CORD_ENDPOINT + "batch", headers=headers, data=request_body)
        
        return response.json()
