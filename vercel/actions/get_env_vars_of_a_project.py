import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class GetEnvVarsRequest(BaseModel):
    project_id_or_name: str = Field(
        ...,
        description="The ID or name of the Vercel project to Get environment variables from. Example: 'project_123'.",
        examples=["project_123"],
    )


class GetEnvVarsResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the environment variables were retrieved successfully. True if the environment variables were retrieved successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the environment variables of the project from the Vercel API.",
    )


class GetEnvVarsAction(Action):
    """
    This action retrieves the environment variables of a specific Vercel project identified by the project ID. The response will include the environment variables as returned by the Vercel API.

    Edge Cases:
    - If the project_id_or_name is not provided in the request, the action will raise a validation error.
    - If the API request to retrieve the environment variables fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Retrieving the environment variables of a Vercel project for configuration purposes.
    - Managing project environment variables within the Vercel platform.
    """

    _display_name = "Get Environment Variables"
    _request_schema = GetEnvVarsRequest
    _response_schema = GetEnvVarsResponse
    _tags = ["vercel", "environment"]
    _tool_name = "vercel"

    def execute(self, request: GetEnvVarsRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        project_id = request.project_id_or_name
        url = f"https://api.vercel.com/v9/projects/{project_id}/env"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
