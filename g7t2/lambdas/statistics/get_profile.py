import os
from decimal import Decimal
import boto3
import json
from entity.assignment import State
from utils.utils import get_endpoint_url, get_user_identifier


def handle(event, context):
    """
    1. get user specific data from dynamodb
    2. create counter dict for solved assignments,
       with following mapping [type][state] = cnt
                         e.g. ['mult']['correct'] = 1
    3. compute grade
    """
    print("statistics-lambda invoked")
    uid = get_user_identifier(event)
    endpoint_url = get_endpoint_url()

    print(f"Called by {uid}")
    # 1. get user data
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)

    data: dict = table.get_item(Key={"UserId": uid})  # type: ignore
    user_data: dict = data["Item"]
    solved_assignments: list[dict] = user_data["Solved"]  # type: ignore
    grades = compute_grades(solved_assignments)
    return_data = {}
    return_data["Results"] = grades
    print(f"{uid}: {json.dumps(return_data, cls=DecimalEncoder)}")

    cognito_client = boto3.client("cognito-idp", endpoint_url=endpoint_url)
    access_token = event["headers"].get("Authorization")
    if access_token is None or not access_token.startswith("Bearer"):
        print("Invalid or missing token")
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Invalid Access Token"}),
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }

    try:
        bearer_keyword_len = len("Bearer ")
        access_token = access_token[bearer_keyword_len:]
        user = cognito_client.get_user(AccessToken=access_token)
        return_data["UserData"] = user["UserAttributes"]
        return {
            "statusCode": 200,
            "body": json.dumps(return_data, cls=DecimalEncoder),
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }
    except cognito_client.exceptions.NotAuthorizedException:
        print("User not authorized")
        return {
            "statusCode": 401,
            "body": json.dumps(return_data, cls=DecimalEncoder),
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }


def compute_grades(solved_assignments: list[dict]):
    types = {assignment["Type"] for assignment in solved_assignments}

    grades = {
        type_: compute_grade_for_type(type_, solved_assignments)
        for type_ in types
    }
    return grades


def compute_grade_for_type(type_, solved_assignments):
    assignments_of_type = [a for a in solved_assignments if a["Type"] == type_]
    correct = sum(
        a["State"] == State.CORRECT.value for a in assignments_of_type
    )
    return {
        "correct": correct,
        "total": len(assignments_of_type),
        "grade": get_grade(correct, len(assignments_of_type)),
    }


def get_grade(correct, total):
    # avoid div. by 0
    if total == 0:
        return 1

    ratio = correct / total
    if ratio > 0.87:
        return 1
    elif ratio > 0.74:
        return 2
    elif ratio > 0.59:
        return 3
    elif ratio > 0.49:
        return 4
    else:
        return 5


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)
