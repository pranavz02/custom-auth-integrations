import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class CreateEnvVarRequest(BaseModel):
    project_id_or_name: str = Field(
        ...,
        description="The ID or name of the Vercel project to which the environment variable(s) will be added. Example: 'project_123'.",
        examples=["project_123"],
    )
    key: str = Field(
        ...,
        description="The key of the environment variable to add. Example: 'API_KEY'.",
        examples=["API_KEY"],
    )
    value: str = Field(
        ...,
        description="The value of the environment variable to add. Example: '12345'.",
        examples=["12345"],
    )
    type_of_env: str = Field(
        ...,
        description="The type of environment variable to add. Example: 'plain'.",
        examples=["plain", "encrypted", "secret", "system", "sensitive"],
    )
    target: list[str] = Field(
        default=None,
        description="The target(s) for the environment variable. Example: ['production', 'development'].",
        examples=[["production", "development", "preview"]],
    )
    comment: str = Field(
        default=None,
        description="A comment for the environment variable.",
        examples=["Database connection string for production"],
    )


class CreateEnvVarResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the environment variable(s) were successfully added to the project. True if the environment variable(s) were added successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the details of the added environment variable(s) from the Vercel API.",
    )


class CreateEnvVarAction(Action):
    """
    This action creates one or more environment variables for a specific Vercel project identified by the project ID. The response will include the details of the added environment variable(s) as returned by the Vercel API.

    Edge Cases:
    - If the project_id or env_vars are not provided in the request, the action will raise a validation error.
    - If the API request to create the environment variable(s) fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Adding environment variables to a Vercel project for configuration purposes.
    - Managing project environment variables within the Vercel platform.
    """

    _display_name = "Create Environment Variables"
    _request_schema = CreateEnvVarRequest
    _response_schema = CreateEnvVarResponse
    _tags = ["vercel", "environment"]
    _tool_name = "vercel"

    def execute(self, request: CreateEnvVarRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        project_id = request.project_id_or_name
        url = f"https://api.vercel.com/v5/projects/{project_id}/env"
        data = {}
        data["key"] = request.key
        data["value"] = request.value
        data["type"] = request.type_of_env
        if request.target:
            data["target"] = request.target
        if request.comment:
            data["comment"] = request.comment

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
