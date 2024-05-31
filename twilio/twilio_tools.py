import requests
from requests.auth import HTTPBasicAuth
from pydantic import BaseModel, Field
from shared.composio_tools.lib import Action, Tool
from typing import List, Optional, Type

class SendSMSRequest(BaseModel):
    account_sid: str = Field(..., description="The Twilio account SID to use for sending the SMS. This must be a valid Twilio account SID. The SID must be in the format ACXXXXXXXX")
    to_number: str = Field(..., description="The phone number to send the SMS to. This must be a valid phone number.", examples=["+XXXXXXXXXXX"])
    from_number: str = Field(..., description="The sender's Twilio phone number (in E.164 format), alphanumeric sender ID, Wireless SIM, short code, or channel address (e.g., +XXXXXXXXXXX). The value of the from parameter must be a sender that is hosted within Twilio and belongs to the Account creating the Message.", examples=["+XXXXXXXXXXX"])
    body: str = Field(..., description="The body of the message to send. This can be a maximum of 1600 characters.")

class SendSMSResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the SMS was sent successfully")

class SendSMS(Action):
    """
    An action to send an SMS message via the Twilio API.
    This action uses the Twilio API to send a text message (SMS) to a specified recipient.
    he SendSMS action allows sending an SMS message through the Twilio API. It uses the SendSMSRequest model to define the input parameters, which include the Twilio account SID, recipient's phone number, sender's phone number, and the message body. The action utilizes authorization data to authenticate the request to Twilio's API endpoint. The action sends a POST request to the Twilio API endpoint with the provided data. The response from the Twilio API is then returned as the output of the action.

    """
    @property
    def display_name(self) -> str:
        return "Send SMS"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return SendSMSRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return SendSMSResponse
    
    def execute(self, request: SendSMSRequest, authorisation_data: dict) -> dict:
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        url = f"https://api.twilio.com/2010-04-01/Accounts/{request.account_sid}/Messages.json"
        # retrieve auth_token from authorisation_data
        auth_token = authorisation_data["headers"]["Authorization"].split(" ")[1]
        
        data = {
            "From": request.from_number,
            "To": request.to_number,
            "Body": request.body
        }
        response = requests.post(url, auth=HTTPBasicAuth(request.account_sid, auth_token), data=data)
        if response.status_code == 201:
            execution_details["executed"] = True
            response_data["success"] = True
        
        response_data["response"] = response.json()

        return {
            "execution_details": execution_details,
            "response_data": response_data
        }
    
class SendWhatsAppMessageRequest(BaseModel):
    account_sid: str = Field(..., description="The Twilio account SID to use for sending the WhatsApp message. This must be a valid Twilio account SID. The SID must be in the format ACXXXXXXXX")
    to_number: str = Field(..., description="The phone number to send the WhatsApp message to. This must be a valid phone number. The value must be in the E.164 format (e.g., +XXXXXXXXXXX).", examples=["+XXXXXXXXXXX"])
    from_number: str = Field(..., description="The sender's Twilio phone number (in E.164 format), alphanumeric sender ID, Wireless SIM, short code, or channel address (e.g., +XXXXXXXXXXX). The value of the from parameter must be a sender that is hosted within Twilio and belongs to the Account creating the Message.", examples=["+XXXXXXXXXXX"])
    body: str = Field(..., description="The body of the message to send. This can be a maximum of 1600 characters.")

class SendWhatsAppMessageResponse(BaseModel):
    success: bool = Field(..., description="Indicates if the WhatsApp message was sent successfully")

class SendWhatsAppMessage(Action):
    """
    Sends a WhatsApp message using the Twilio API. 
    This action uses the Twilio API to send a WhatsApp message to a specified recipient. The SendWhatsAppMessage action allows sending a WhatsApp message through the Twilio API. It uses the SendWhatsAppMessageRequest model to define the input parameters, which include the Twilio account SID, recipient's phone number, sender's phone number, and the message body. The action utilizes authorization data to authenticate the request to Twilio's API endpoint. The action sends a POST request to the Twilio API endpoint with the provided data. The response from the Twilio API is then returned as the output of the action.
    """
    @property
    def display_name(self) -> str:
        return "Send WhatsApp Message"
    
    @property
    def request_schema(self) -> Type[BaseModel]:
        return SendWhatsAppMessageRequest
    
    @property
    def response_schema(self) -> Type[BaseModel]:
        return SendWhatsAppMessageResponse
    
    def execute(self, request: SendWhatsAppMessageRequest, authorisation_data: dict) -> dict:
        execution_details = {"executed": False}
        response_data = {"success": False, "response": None}
        url = f"https://api.twilio.com/2010-04-01/Accounts/{request.account_sid}/Messages.json"
        # retrieve auth_token from authorisation_data
        auth_token = authorisation_data["headers"]["Authorization"].split(" ")[1]
        
        data = {
            "To": f"whatsapp:{request.to_number}",
            "From": f"whatsapp:{request.from_number}",
            "Body": request.body
        }
        response = requests.post(url, auth=HTTPBasicAuth(request.account_sid, auth_token), data=data)
        if response.status_code == 201:
            execution_details["executed"] = True
            response_data["success"] = True
        
        response_data["response"] = response.json()

        return {
            "execution_details": execution_details,
            "response_data": response_data
        }

class Twilio(Tool):
    """
    Twilio API tool
    """
    def actions(self) -> list:
        return[
            SendSMS, SendWhatsAppMessage
        ]
    
    def triggers(self) -> list:
        return []
    
__all__ = ["Twilio"]