import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class EditEnvVarRequest(BaseModel):
    project_id_or_name: str = Field(
        ...,
        description="The ID or name of the Vercel project to which the environment variable belongs. Example: 'project_123'.",
        examples=["project_123"],
    )
    env_var_id: str = Field(
        ...,
        description="The ID of the environment variable to edit. Example: 'env_456'.",
        examples=["env_456"],
    )
    key: str = Field(
        default=None,
        description="The key of the environment variable. Example: 'API_KEY'.",
        examples=["API_KEY"],
    )
    value: str = Field(
        default=None,
        description="The new value of the environment variable. Example: '67890'.",
        examples=["67890"],
    )
    type_of_env: str = Field(
        default=None,
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


class EditEnvVarResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the environment variable was edited successfully. True if the environment variable was edited successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the details of the edited environment variable from the Vercel API.",
    )


class EditEnvVarAction(Action):
    """
    This action edits an existing environment variable for a specific Vercel project identified by the project ID and environment variable ID. The response will include the details of the edited environment variable as returned by the Vercel API.

    Edge Cases:
    - If the project_id, env_var_id, are not provided in the request, the action will raise a validation error.
    - If the API request to edit the environment variable fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Editing the value of an environment variable for a Vercel project.
    - Managing project environment variables within the Vercel platform.
    """

    _display_name = "Edit Environment Variable"
    _request_schema = EditEnvVarRequest
    _response_schema = EditEnvVarResponse
    _tags = ["vercel", "environment"]
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

    def execute(self, request: EditEnvVarRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        project_id = request.project_id_or_name
        env_var_id = request.env_var_id
        url = f"https://api.vercel.com/v9/projects/{project_id}/env/{env_var_id}"
        data = {}
        if request.key:
            data["key"] = request.key
        if request.value:
            data["value"] = request.value
        if request.type_of_env:
            data["type"] = request.type_of_env
        if request.target:
            data["target"] = request.target
        if request.comment:
            data["comment"] = request.comment

        try:
            response = requests.patch(url, headers=headers, json=data)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
