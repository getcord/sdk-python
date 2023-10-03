from enum import Enum
import json


class Status(Enum):
    ACTIVE = "active"
    DELETED = "deleted"


class PlatformUserVariables:
    def __init__(self, id: str, email: str, name: str = None, short_name: str = None, status: Status = None, profile_picture_url: str = None, metadata: json = {}):
        self.id = id
        self.email = email
        self.name = name
        self.shortName = short_name
        self.status = status
        self.profilePictureURL = profile_picture_url
        self.metadata = metadata


class PlatformOrganizationVariables:
    def __init__(self, id: str, name: str, status: Status = None, members: list[str] = None):
        self.id = id
        self.name = name
        self.status = status
        self.members = members


class ClientAuthTokenData:
    def __init__(self, user_id: str, organization_id: str, user_details: PlatformUserVariables = None, organization_details: PlatformOrganizationVariables = None):
        self.user_id = user_id
        self.organization_id = organization_id
        self.user_details = user_details
        if self.user_details and self.user_details.id:
            delattr(self.user_details, 'id')
        self.organization_details = organization_details
        if self.organization_details and self.organization_details.id:
            delattr(self.organization_details, 'id')
