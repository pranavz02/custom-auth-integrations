import requests
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action


class AddDomainRequest(BaseModel):
    project_id_or_name: str = Field(
        ...,
        description="The ID or name of the Vercel project to which the domain will be added. Example: 'project_123'.",
        examples=["project_123"],
    )
    domain_name: str = Field(
        ...,
        description="The domain name to add to the project. Example: 'example.com'.",
        examples=["example.com"],
    )
    gitBranch: str = Field(
        default=None,
        description="The Git branch to deploy the domain from. Example: 'main'.",
        examples=["main"],
    )
    redirect: str = Field(
        default=None,
        description="Target destination for the domain redirect.",
        examples=["https://example.com"],
    )
    redirectStatusCode: int = Field(
        default=None,
        description="The status code for the domain redirect.",
        examples=[301, 302, 307, 308],
    )


class AddDomainResponse(BaseModel):
    success: bool = Field(
        ...,
        description="Indicates if the domain was successfully added to the project. True if the domain was added successfully.",
    )
    response: dict = Field(
        ...,
        description="The JSON response containing the details of the added domain from the Vercel API.",
    )


class AddDomainAction(Action):
    """
    This action adds a domain to a specific Vercel project identified by the project ID. The response will include the details of the added domain as returned by the Vercel API.

    Edge Cases:
    - If the project_id or domain_name is not provided in the request, the action will raise a validation error.
    - If the API request to add the domain fails, the action will return a response with `success` set to `false` and `response` set to `None`.

    Use Cases:
    - Adding a custom domain to a Vercel project for deployment purposes.
    - Managing project domains within the Vercel platform.
    """

    _display_name = "Add Domain to Project"
    _request_schema = AddDomainRequest
    _response_schema = AddDomainResponse
    _tags = ["vercel", "domain"]
    _tool_name = "vercel"

    def execute(self, request: AddDomainRequest, authorisation_data: dict) -> dict:
        headers = authorisation_data["headers"]
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        project_id = request.project_id_or_name
        domain_name = request.domain_name
        data = {}
        if request.gitBranch:
            data["gitBranch"] = request.gitBranch
        if request.redirect:
            data["redirect"] = request.redirect
        if request.redirectStatusCode:
            data["redirectStatusCode"] = request.redirectStatusCode

        data["name"] = domain_name
        url = f"https://api.vercel.com/v10/projects/{project_id}/domains"

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            execution_details["executed"] = True
            response_data["success"] = True
            response_data["response"] = response.json()

        except Exception as e:
            response_data["response"] = str(e)

        return {"execution_details": execution_details, "response_data": response_data}
