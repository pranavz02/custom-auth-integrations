import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class FindProjectRequest(BaseModel):
    project_id_or_name: str = Field(
        ...,
        description="The ID or name of the Vercel project to find. Example: 'project_123'.",
        examples=["project_123"],
    )


class FindProjectResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the project was found successfully. True if the project was found successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the details of the found project from the Vercel API.",
    )


class FindProjectAction(Action):
    """
    This action finds a specific Vercel project by its ID or name. The response will include the details of the found project as returned by the Vercel API.

    Edge Cases:
    - If project_id is provided in the request, the action will raise a validation error.
    - If the API request to find the project fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Finding a Vercel project by its ID or name for management purposes.
    - Retrieving project details within the Vercel platform.
    """

    _display_name = "Find Project"
    _request_schema = FindProjectRequest
    _response_schema = FindProjectResponse
    _tags = ["vercel", "project"]
    _tool_name = "vercel"

    @property
    def display_name(self) -> str:
        return self._display_name
    
    @property   
    def request_schema(self) -> BaseModel:
        return self._request_schema
    
    @property
    def response_schema(self) -> BaseModel:
        return self._response_schema

    def execute(self, request: FindProjectRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        url = f"https://api.vercel.com/v5/projects/{request.project_id_or_name}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
