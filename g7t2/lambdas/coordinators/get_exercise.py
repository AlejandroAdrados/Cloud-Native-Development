import json
import boto3
import os
import utils.utils as utils
from decimal import Decimal


def handle(event, context):
    """
    Returns a single assignment for a specific user.
    The assignment type can be specified via queryStringParameters.
    The default type is addition.
    """
    print("get-exercise invoked")

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }

    # get requested assignment type and userid
    requested_type = "ADD"
    if (
        "queryStringParameters" in event
        and "type" in event["queryStringParameters"]
    ):
        requested_type = event["queryStringParameters"]["type"]
    sub = utils.get_user_identifier(event)

    # fetch unsovled assignments for user
    endpoint_url = utils.get_endpoint_url()
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)  # type: ignore
    data: dict = table.get_item(Key={"UserId": sub})
    user_data: dict = data["Item"]
    unsolved_assignments: list[dict] = user_data["Unsolved"]

    # return first unsolved assignment of requested type
    for assignment in unsolved_assignments:
        if assignment["Type"] == requested_type:
            return {
                "statusCode": 200,
                "body": json.dumps(assignment, cls=DecimalEncoder),
                "headers": headers,
                "isBase64Encoded": False,
            }
    return {
        "statusCode": 204,
        "body": "",
        "headers": headers,
        "isBase64Encoded": False,
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)
