import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class DeleteProjectRequest(BaseModel):
    project_id_or_name: str = Field(
        ...,
        description="The ID of the Vercel project to delete. Example: 'project_123'.",
        examples=["project_123"],
    )


class DeleteProjectResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the project was deleted successfully. True if the project was deleted successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the result of the delete operation from the Vercel API.",
    )


class DeleteProjectAction(Action):
    """
    This action deletes a specific Vercel project identified by the project ID. The response will include the result of the delete operation as returned by the Vercel API.

    Edge Cases:
    - If the project_id is not provided in the request, the action will raise a validation error.
    - If the API request to delete the project fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Deleting a Vercel project that is no longer needed.
    - Managing project lifecycle within the Vercel platform.
    """

    _display_name = "Delete Project"
    _request_schema = DeleteProjectRequest
    _response_schema = DeleteProjectResponse
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

    def execute(self, request: DeleteProjectRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        project_id = request.project_id_or_name
        url = f"https://api.vercel.com/v9/projects/{project_id}"

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
