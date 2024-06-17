import requests
from pydantic import BaseModel, Field
from composio_tools import Action, Tool
from typing import Optional, Type
import json

class CreateURLRequest(BaseModel):
    url: str = Field(..., description="URL to shorten")
    domain: str = Field(None, description="Custom domain to use")
    description: str = Field(None, description="Description of the shortened URL")

class CreateURLResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    short_url: str = Field(None, description="Shortened URL") 
    data: dict = Field(None, description="Data returned from the API")

class TinyurlCreateURL(Action):
    """
    Create a shortened URL using TinyURL
    """
    @property
    def display_name(self) -> str:
        return "Create URL"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return CreateURLRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return CreateURLResponse

    def execute(self, request_data: request_schema, authorisation_data: dict) -> CreateURLResponse:
        headers = authorisation_data["headers"]
        data = {
            "url": request_data.url,
            "domain": request_data.domain,
            "description": request_data.description
        }
        
        response = requests.post("https://api.tinyurl.com/create", headers=headers, json=data)
        response_json = response.json()
        data = response_json.get("data", {})
        tiny_url = data.get("tiny_url", None)
        if response.status_code != 200:
            return CreateURLResponse(success=False, short_url=None, data=response_json)
        
        return CreateURLResponse(success=True, short_url=tiny_url, data=data)
    
class UpdateURLRequest(BaseModel):
    domain: str = Field(None, description="Custom domain to use")
    new_domain: str = Field(..., description="New custom domain to use")
    new_description: str = Field(None, description="New description of the shortened URL")
    new_stats: bool = Field(None, description="Whether to enable statistics for the shortened URL")

class UpdateURLResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    short_url: str = Field(None, description="Shortened URL")
    data: dict = Field(None, description="Data returned from the API")

class TinyurlUpdateURL(Action):
    """
    Update a shortened URL using TinyURL
    """
    @property
    def display_name(self) -> str:
        return "Update URL"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return UpdateURLRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return UpdateURLResponse

    def execute(self, request_data: request_schema, authorisation_data: dict) -> UpdateURLResponse:
        headers = authorisation_data["headers"]
        data = {
            "domain": request_data.domain,
            "new_domain": request_data.new_domain,
            "new_description": request_data.new_description,
            "new_stats": request_data.new_stats
        }
        
        response = requests.post("https://api.tinyurl.com/update", headers=headers, json=data)
        response_json = response.json()
        data = response_json.get("data", {})
        tiny_url = data.get("tiny_url", None)
        if response.status_code != 200:
            return UpdateURLResponse(success=False, short_url=None, data=response_json)
        
        return UpdateURLResponse(success=True, short_url=tiny_url, data=data)
    
# update tinyurl's long url
class UpdateLongURLRequest(BaseModel):
    domain: str = Field(None, description="Custom domain to use")
    url: str = Field(..., description="New URL to shorten")

class UpdateLongURLResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    short_url: str = Field(None, description="Shortened URL")
    data: dict = Field(None, description="Data returned from the API")

class TinyurlUpdateLongURL(Action):
    """
    Update the long URL of a shortened URL using TinyURL
    """
    @property
    def display_name(self) -> str:
        return "Update Long URL"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return UpdateLongURLRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return UpdateLongURLResponse

    def execute(self, request_data: request_schema, authorisation_data: dict) -> UpdateLongURLResponse:
        headers = authorisation_data["headers"]
        data = {
            "domain": request_data.domain,
            "url": request_data.url
        }
        
        response = requests.post("https://api.tinyurl.com/change", headers=headers, json=data)
        response_json = response.json()
        data = response_json.get("data", {})
        tiny_url = data.get("tiny_url", None)
        if response.status_code != 200:
            return UpdateLongURLResponse(success=False, short_url=None, data=response_json)
        
        return UpdateLongURLResponse(success=True, short_url=tiny_url, data=data)
    
# Endpoint allows to receive TinyURL information
class GetURLRequest(BaseModel):
    domain: str = Field(None, description="Custom domain to use")
    alias: str = Field(..., description="URL to shorten")

class GetURLResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    data: dict = Field(None, description="Data returned from the API")

class TinyurlGetURL(Action):
    """
    Get information about a shortened URL using TinyURL
    """
    @property
    def display_name(self) -> str:
        return "Get URL"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return GetURLRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return GetURLResponse

    def execute(self, request_data: request_schema, authorisation_data: dict) -> GetURLResponse:
        headers = authorisation_data["headers"]
        domain = request_data.domain    
        alias = request_data.alias
        response = requests.get(f"https://api.tinyurl.com/alias/{domain}/{alias}", headers=headers)

        response_json = response.json()
        data = response_json.get("data", {})
        if response.status_code != 200:
            return GetURLResponse(success=False, data=response_json)
        
        return GetURLResponse(success=True, data=data)
    
#delete tinyurl
class DeleteURLRequest(BaseModel):
    domain: str = Field(None, description="Custom domain to use")
    alias: str = Field(..., description="URL to shorten")

class DeleteURLResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    data: dict = Field(None, description="Data returned from the API")

class TinyurlDeleteURL(Action):
    """
    Delete a shortened URL using TinyURL
    """
    @property
    def display_name(self) -> str:
        return "Delete URL"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return DeleteURLRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return DeleteURLResponse

    def execute(self, request_data: request_schema, authorisation_data: dict) -> DeleteURLResponse:
        headers = authorisation_data["headers"]
        domain = request_data.domain    
        alias = request_data.alias
        response = requests.delete(f"https://api.tinyurl.com/alias/{domain}/{alias}", headers=headers)

        response_json = response.json()
        data = response_json.get("data", {})
        if response.status_code != 200:
            return DeleteURLResponse(success=False, data=response_json)
        
        return DeleteURLResponse(success=True, data=data)
    
# get all tinyurls
class GetAllURLRequest(BaseModel):
    type: str = Field(None, description="Aliases list type, Available values : available, archived")
    from_date: str = Field(None, description="Datetime, indicating that only TinyURLs created after the datetime will be selected.")
    to_date: str = Field(None, description="Datetime, indicating that only TinyURLs created before the datetime will be selected.")
    search: str = Field(None, description="Search for tags and alias")

class Tinyurl(Tool):
    def actions(self) -> list:
        return [
            TinyurlCreateURL,
            TinyurlUpdateURL,


        ]
    
    def triggers(self) -> list:
        return []
    
__all__ = ['Tinyurl']

def test_function():
    # tests all the actions separately with dummy data
    authorisation_data = {
        "headers": {
            "Authorization": "Bearer FJBEKKBLm0f7sp6bmSzEM77zLdm6Dg78S5waRkAs5wDXsa6adOP6vSrcb19G",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    }
    # action1 = TinyurlCreateURL()
    # request_data = CreateURLRequest(url="https://google.com", domain="tinyurl.com", alias="google", description="Google search")
    # response = action1.execute(request_data, authorisation_data)
    # print(response)

    action2 = TinyurlUpdateURL()
    request_data = UpdateURLRequest(domain="tinyurl.com", new_domain="tinyurl.com", new_description="Google search engine", new_stats=True)
    response = action2.execute(request_data, authorisation_data)
    print(response)

test_function()