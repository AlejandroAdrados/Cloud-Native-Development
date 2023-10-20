import os
import uuid
from io import BytesIO

import boto3

from utils.utils import get_endpoint_url, parse_multipart_form_data


def handle(event, context):
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }
    cognito_client = boto3.client(
        "cognito-idp", endpoint_url=get_endpoint_url()
    )

    form_data = parse_multipart_form_data(event)

    required_properties = ["username", "password", "given_name", "family_name"]

    missing = [
        property
        for property in required_properties
        if property not in form_data
    ]

    if len(missing) != 0:
        return {
            "statusCode": 400,
            "body": {"error": f"{', '.join(missing)} missing from form data"},
            "headers": headers,
        }

    profile_picture_key = (
        str(uuid.uuid4())
        if "profile_picture" in form_data
        and len(form_data["profile_picture"].value) != 0
        else "null"
    )

    if (
        "profile_picture" in form_data
        and len(form_data["profile_picture"].value) != 0
    ):
        s3_client = boto3.client("s3", endpoint_url=get_endpoint_url())
        s3_client.upload_fileobj(
            BytesIO(form_data["profile_picture"].value),
            os.environ["PROFILE_PICUTRE_BUCKET_NAME"],
            # type checker does not realize this is never None
            profile_picture_key,  # type: ignore
        )

    try:
        response = cognito_client.sign_up(
            ClientId=os.environ["COGNITO_CLIENT_ID"],
            Username=form_data["username"].value,
            Password=form_data["password"].value,
            UserAttributes=[
                {"Name": "given_name", "Value": form_data["given_name"].value},
                {
                    "Name": "family_name",
                    "Value": form_data["family_name"].value,
                },
                {
                    "Name": "custom:profile_picture",
                    "Value": profile_picture_key,
                },
            ],
        )
    except cognito_client.exceptions.UsernameExistsException:
        print(f"User {form_data['username'].value} already exists.")
        return {
            "statusCode": 400,
            "body": {"error": "User with that username already exists."},
            "headers": headers,
        }
    except cognito_client.exceptions.InvalidParameterException:
        return {
            "statusCode": 400,
            "body": {"error": "Invalid password"},
            "headers": headers,
        }

    return {
        "statusCode": 201,
        "body": {
            "message": "Successfully signed up the user",
            "user": {"sub": response["UserSub"]},
        },
        "headers": headers,
    }
