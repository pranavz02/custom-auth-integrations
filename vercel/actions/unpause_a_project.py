import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class UnpauseProjectRequest(BaseModel):
    project_id: str = Field(
        ...,
        description="The ID of the Vercel project to unpause. Example: 'project_123'.",
        examples=["project_123"],
    )


class UnpauseProjectResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the project was unpaused successfully. True if the project was unpaused successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the result of the unpause operation from the Vercel API.",
    )


class UnpauseProjectAction(Action):
    """
    This action unpauses a specific Vercel project identified by the project ID. The response will include the result of the unpause operation as returned by the Vercel API.

    Edge Cases:
    - If the project_id is not provided in the request, the action will raise a validation error.
    - If the API request to unpause the project fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Unpausing a Vercel project to resume its operation.
    - Managing project lifecycle within the Vercel platform.
    """

    _display_name = "Unpause Project"
    _request_schema = UnpauseProjectRequest
    _response_schema = UnpauseProjectResponse
    _tags = ["vercel", "project"]
    _tool_name = "vercel"

    @property
    def display_name(self):
        return self._display_name
    
    @property   
    def request_schema(self):
        return self._request_schema
    
    @property
    def response_schema(self):
        return self._response_schema

    def execute(self, request: UnpauseProjectRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        project_id = request.project_id
        url = f"https://api.vercel.com/v5/projects/{project_id}/unpause"

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
