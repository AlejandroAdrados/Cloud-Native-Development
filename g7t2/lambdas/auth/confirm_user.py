import json
import os

import boto3

from utils.utils import get_endpoint_url


def handle(event, context):

    cognito_client = boto3.client(
        "cognito-idp", endpoint_url=get_endpoint_url()
    )

    unparsed_body = event["body"]

    body = json.loads(unparsed_body) if unparsed_body else {}
    code = body.get("code")
    username = body.get("username")

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }

    required_properties = ["code", "username"]
    missing = [
        p for p in required_properties if p not in body or p is body[p] is None
    ]

    if code is None or username is None:
        return {
            "statusCode": 400,
            "body": {
                "error": f"{', '.join(missing)} missing from request body"
            },
            "headers": headers,
            "isBase64Encoded": False,
        }
    try:
        cognito_client.confirm_sign_up(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            Username=username,
            ConfirmationCode=code,
        )
        return {
            "statusCode": 200,
            "body": {"message": "Successfully confirmed sign up"},
            "headers": headers,
            "isBase64Encoded": False,
        }
    except cognito_client.exceptions.CodeMismatchException:
        return {
            "statusCode": 400,
            "body": {"error": "Incorrect authentication code"},
            "headers": headers,
            "isBase64Encoded": False,
        }
    except cognito_client.exceptions.UserNotFoundException:
        return {
            "statusCode": 400,
            "body": {"error": "No such user"},
            "headers": headers,
            "isBase64Encoded": False,
        }
