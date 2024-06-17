import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class UpdateProjectRequest(BaseModel):
    project_id: str = Field(
        ...,
        description="The ID of the Vercel project to update. Example: 'project_123'.",
        examples=["project_123"],
    )
    name: str = Field(
        default=None,
        description="The new name of the Vercel project. Example: 'updated-project'.",
        examples=["updated-project"],
    )
    framework: str = Field(
        default=None,
        description="The framework of the project",
        examples=[
            "blitzjs",
            "nextjs",
            "gatsby",
            "remix",
            "astro",
            "hexo",
            "eleventy",
            "docusaurus-2",
            "docusaurus",
            "preact",
            "solidstart-1",
            "solidstart",
            "dojo",
            "ember",
            "vue",
            "scully",
            "ionic-angular",
            "angular",
            "polymer",
            "svelte",
            "sveltekit",
            "sveltekit-1",
            "ionic-react",
            "create-react-app",
            "gridsome",
            "umijs",
            "sapper",
            "saber",
            "stencil",
            "nuxtjs",
            "redwoodjs",
            "hugo",
            "jekyll",
            "brunch",
            "middleman",
            "zola",
            "hydrogen",
            "vite",
            "vitepress",
            "vuepress",
            "parcel",
            "sanity",
            "storybook",
        ],
    )


class UpdateProjectResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the project was updated successfully. True if the project was updated successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the details of the updated project from the Vercel API.",
    )


class UpdateProjectAction(Action):
    """
    This action updates an existing Vercel project identified by the project ID. The response will include the details of the updated project as returned by the Vercel API.

    Edge Cases:
    - If the project_id is not provided in the request, the action will raise a validation error.
    - If the API request to update the project fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Updating the details of a Vercel project for configuration purposes.
    - Managing project details within the Vercel platform.
    """

    _display_name = "Update Project"
    _request_schema = UpdateProjectRequest
    _response_schema = UpdateProjectResponse
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

    def execute(self, request: UpdateProjectRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        project_id = request.project_id
        url = f"https://api.vercel.com/v5/projects/{project_id}"
        data = {}
        if request.name:
            data["name"] = request.name
        if request.framework:
            data["framework"] = request.framework

        try:
            response = requests.patch(url, headers=headers, json=data)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
