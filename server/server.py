import datetime
from enum import Enum
import json
import jwt
import requests

class status(Enum):
    ACTIVE = "active"
    DELETED = "deleted"

class platformUserVariables:
    def __init__(self, email: str, name: str = None, status: status = None, profile_picture_url: str = None, first_name: str = None, last_name: str = None, id: str = None):
        self.email = email
        self.name = name
        self.status = status
        self.profile_picture_url = profile_picture_url
        self.first_name = first_name
        self.last_name = last_name
        self.id = id

class platformOrganizationVariables:
    def __init__(self, name: str, status: status = None, members: list[str] = None, id: str = None):
        self.name = name
        self.status = status
        self.members = members
        self.id = id

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

def sync_cord_user(app_id: str, secret: str, user_id: str, user: platformUserVariables):
    auth_token: str = get_server_auth_token(app_id, secret)

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json"
    }
    response = requests.put("https://api.cord.com/v1/users/" + user_id, headers=headers, data=toJson(user))

    return response.json()

def sync_cord_organization(app_id: str, secret: str, org_id: str, organization: platformOrganizationVariables):
    auth_token: str = get_server_auth_token(app_id, secret)

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json"
    }
    response = requests.put("https://api.cord.com/v1/organizations/" + org_id, headers=headers, data=toJson(organization))

    return response.json()

def batch_sync_cord_users_and_organizations(app_id: str, secret: str, users: list[platformUserVariables], organizations: list[platformOrganizationVariables]):
    auth_token: str = get_server_auth_token(app_id, secret)

    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "Content-Type": "application/json"
    }
    request_body = "{{ \"organizations\": {}, \"users\": {} }}".format(toJson(organizations), toJson(users))
    response = requests.post("https://api.cord.com/v1/batch", headers=headers, data=request_body)
    
    return response.json()


print(sync_cord_user("1ac6151f-622e-4b71-9f4d-fbfd3339ba39", "730f61aa965fb520a59a5fd63aa2b092", "1", platformUserVariables("nick@cord.com")))
print(sync_cord_organization("1ac6151f-622e-4b71-9f4d-fbfd3339ba39", "730f61aa965fb520a59a5fd63aa2b092", "1", platformOrganizationVariables("org1")))
print(batch_sync_cord_users_and_organizations("1ac6151f-622e-4b71-9f4d-fbfd3339ba39", "730f61aa965fb520a59a5fd63aa2b092", [ platformUserVariables("nick@cord.com", None, None, None, None, None, "1") ], [ platformOrganizationVariables("org1", None, None, "1")]))
