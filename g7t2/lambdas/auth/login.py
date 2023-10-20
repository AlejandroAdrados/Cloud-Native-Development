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
    username = body.get("username")
    password = body.get("password")

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }

    required_properties = ["password", "username"]
    missing = [
        p for p in required_properties if p not in body or p is body[p] is None
    ]

    if password is None or username is None:
        return {
            "statusCode": 400,
            "body": {
                "error": f"{', '.join(missing)} missing from request body"
            },
            "headers": headers,
            "isBase64Encoded": False,
        }

    try:
        auth_result = cognito_client.initiate_auth(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )
        return {
            "statusCode": 200,
            "body": auth_result["AuthenticationResult"],
            "headers": headers,
            "isBase64Encoded": False,
        }
    except cognito_client.exceptions.UserNotFoundException:
        return {
            "statusCode": 400,
            "body": {"error": "Username or password incorrect"},
            "headers": headers,
            "isBase64Encoded": False,
        }
    except cognito_client.exceptions.UserNotConfirmedException:
        return {
            "statusCode": 400,
            "body": {"error": "Account is unconfirmed"},
            "headers": headers,
            "isBase64Encoded": False,
        }
    except cognito_client.exceptions.NotAuthorizedException:
        return {
            "statusCode": 400,
            "body": {
                "error": "Username or password incorrect",
            },
            "headers": headers,
            "isBase64Encoded": False,
        }
