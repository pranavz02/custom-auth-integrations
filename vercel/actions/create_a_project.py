import json
import os

import requests
from pydantic import BaseModel, Field

from shared.composio_tools.lib import Action


class CreateProjectRequest(BaseModel):
    name: str = Field(
        ...,
        description="The name of the project in less than 100 characters.",
        examples=["composio"],
    )
    description: str = Field(
        default=None,
        description="The description of the project",
        examples=["The project to create a project"],
    )
    buildCommand: str = Field(
        default=None,
        description="The build command to run the project",
        examples=["npm run build"],
    )
    commandForIgnoringBuildStep: str = Field(
        default=None,
        description="The command to ignore the build step",
        examples=["npm run build"],
    )
    devCommand: str = Field(
        default=None,
        description="The dev command to run the project",
        examples=["npm run dev"],
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
    # gitRepository should be an object with repo name and type
    gitRepositoryName: str = Field(
        ..., description="The name of the git repository", examples=["username/repo"]
    )
    # add enum values in gitRepositoryType
    gitRepositoryType: str = Field(
        ...,
        description="The type of the git repository",
        examples=["github", "gitlab", "bitbucket"],
    )
    installCommand: str = Field(
        default=None,
        description="The install command to run the project",
        examples=["npm install"],
    )
    outputDirectory: str = Field(
        default=None,
        description="The output directory of the project",
        examples=["dist"],
    )
    publicSource: bool = Field(
        default=False,
        description="Specifies whether the source code and logs of the deployments for this project should be public or not",
        examples=[True, False],
    )
    rootDirectory: str = Field(
        default=None,
        description="The root directory of the project. When null is used it will default to the project root",
        examples=["."],
    )
    serverlessFunctionRegion: str = Field(
        default=None,
        description="The region to deploy the serverless function",
        examples=["us-east-1"],
    )
    # environmentVariables should be an object with key value pair


class CreateProjectResponse(BaseModel):
    success: bool = Field(
        ..., description="The success of the project creation", examples=[True, False]
    )
    response: str = Field(..., description="The response of the project creation")


class CreateProjectAction(Action):
    """
    A class representing an action to create a project.

    This class encapsulates the logic for creating a project in the Vercel platform. It provides methods to interact with the Vercel API and perform the necessary operations to create a project.

    Use cases:
    - Create a new project in the Vercel platform
    - Specify the project details such as name, description, build command, etc.
    - Set up the project with the required configuration and settings
    - Deploy the project to the Vercel platform

    Edge cases:
    - The action fails if the project creation request is invalid or incomplete
    - The action fails if the project creation request is not authorized or authenticated
    """

    _display_name = "Create a project"
    _request_schema = CreateProjectRequest
    _response_schema = CreateProjectResponse
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

    def execute(self, authorisation_data: dict, request: CreateProjectRequest) -> dict:
        token = authorisation_data["headers"]["Authorization"].split(" ")[1]
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}

        url = "https://api.vercel.com/v12/projects"
        data = {
            "name": request.name,
            "description": request.description,
            "buildCommand": request.buildCommand,
            "commandForIgnoringBuildStep": request.commandForIgnoringBuildStep,
            "devCommand": request.devCommand,
            "framework": request.framework,
            "gitRepository": {
                "name": request.gitRepositoryName,
                "type": request.gitRepositoryType,
            },
            "installCommand": request.installCommand,
            "outputDirectory": request.outputDirectory,
            "publicSource": request.publicSource,
            "rootDirectory": request.rootDirectory,
            "serverlessFunctionRegion": request.serverlessFunctionRegion,
            # "environmentVariables": request.environmentVariables
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            response_data["success"] = True
            response_data["response"] = response.json()
            execution_details["executed"] = True

        except Exception as error:
            response_data["response"] = str(error)

        return {"execution_details": execution_details, "response_data": response_data}
