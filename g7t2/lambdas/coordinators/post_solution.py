import json
import os
import boto3
from utils.utils import get_user_identifier, get_endpoint_url


def handle(event, context):
    """
    Publishes user solution to corresponding evaluator.
    """
    print("post_solution invoked")

    headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }

    # get attributes from user request
    body = json.loads(event["body"])
    uid = get_user_identifier(event)

    required = ["assignmentId", "assignmentType", "solution"]
    missing = [p for p in required if p not in body]

    if len(missing) != 0:
        error = f"{','.join(missing)} are required but missing from body"
        return {
            "statusCode": 400,
            "body": {"error": error},
            "headers": headers,
            "isBase64Encoded": False,
        }

    assignment_id = body["assignmentId"]
    assignment_type = body["assignmentType"]
    submitted_solution = body["solution"]
    # uid = "2544b3f3-ca60-4ee4-9175-3ae772aaf624"
    # assignment_id = "ae167040-01f9-4073-adbd-395f9ea9acf4"
    # assignment_type = "ADD"
    # submitted_solution = "5"
    message = {
        "assignment_id": assignment_id,
        "solution": submitted_solution,
        "sub": uid,
    }

    # load correct sns topic
    sns_client = boto3.client("sns", endpoint_url=get_endpoint_url())
    sns_topic = ""
    if assignment_type == "ADD":
        sns_topic = os.environ.get("ADD_EVAL")
    elif assignment_type == "MULT":
        sns_topic = os.environ.get("MULT_EVAL")
    elif assignment_type == "DERIV":
        sns_topic = os.environ.get("DERIV_EVAL")

    # publish solution to sns
    try:
        sns_client.publish(
            TopicArn=sns_topic,
            Message=json.dumps(message),
        )
        print(f"Successfully published to {sns_topic}")
    except sns_client.meta.client.exceptions.NotFoundException:
        print(f"Unable to find topic with arc {sns_topic}")

    return {
        "statusCode": 200,
        "body": {},
        "headers": headers,
        "isBase64Encoded": False,
    }
