import os
from random import randint
from entity.assignment import Assignment, State, Type
from typing import Any
from io import BytesIO
import base64
from cgi import FieldStorage


def get_endpoint_url():
    """
    Returns the endpoint url of the localstack environment.
    """
    hostname = os.environ.get("LOCALSTACK_HOSTNAME", "localstack")
    return f"http://{hostname}:4566"


def get_user_identifier(event: dict[str, Any]):
    """
    Returns the user identifier from the lambda event dictionary.

    Args:
        - event: A dictionary containing the lambda event data.

    Returns:
        A string representing the user identifier.

    Raises:
        KeyError: If the event dictionary does not contain the necessary data.
    """
    sub = event["requestContext"]["identity"]["cognitoIdentityId"]
    return sub


def list_to_dynamo_list(nums: list):
    dynamo_list = []
    for num in nums:
        dynamo_list.append({"N": str(num)})
    return dynamo_list


def persist_assignment(
    dynamodb, table_name: str, assignment: Assignment, uid: str
):
    """
    Persists an assignment for a specific user.

    Args:
        - dynamodb: boto3 dynamodb client
        - table_name: name of the table
        - assignment: assignment that will be persisted
        - uid: id of user for whom the assignment will be persisted
    """
    update_expression = (
        "SET #list ="
        "list_append"
        "(if_not_exists"
        "(#list, :empty_list), :assignment)"
    )
    # persist assignment to either 'Unsolved' or 'Solved'
    # list depending on the state of the assignment
    list_type = "Unsolved" if assignment.state == State.UNSOLVED else "Solved"
    result = dynamodb.update_item(
        TableName=table_name,
        Key={"UserId": {"S": uid}},
        UpdateExpression=update_expression,
        ExpressionAttributeNames={"#list": list_type},
        ExpressionAttributeValues={
            ":assignment": {
                "L": [
                    {
                        "M": {
                            "Id": {"S": str(assignment.id)},
                            "Type": {"S": str(assignment.type.value)},
                            "Content": {"L": assignment.content},
                            "State": {"S": str(assignment.state.value)},
                        }
                    }
                ]
            },
            ":empty_list": {"L": []},
        },
        ReturnValues="UPDATED_NEW",
    )
    print(f"persist_assignment for userid: {uid}")
    print(result)


def remove_assignment(dynamodb, assignment_index: int, uid: str):
    """
    Persists an assignment for a specific user.

    Args:
        - dynamodb: boto3 dynamodb client
        - assignment_index: index in assignment list
        - uid: user id
    """
    item_key = {"UserId": {"S": str(uid)}}
    update_expression = f"REMOVE Unsolved[{assignment_index}]"
    dynamodb.update_item(
        TableName=os.environ["TABLE_NAME"],
        Key=item_key,
        UpdateExpression=update_expression,
    )


def parse_multipart_form_data(event):
    """Parses a multipart form data payload from an HTTP event.

    Args:
        event (dict): The HTTP event object containing the form data payload.
            The event must contain a "headers" key with a "Content-Type"
            value and a "body" key with the form data payload
            in base64-encoded format.

    Returns:
        dict: A dictionary containing the key-value pairs
            of the parsed form data. If a form field has multiple values,
            only the first value is retained in the returned dictionary.

    Raises:
        ValueError: If the "Content-Type" header is not present in the event
            or is not of the multipart form data type.
    """
    # content_type = event["headers"].get("Content-Type", "") or event[
    #     "headers"
    # ].get("content-type", "")
    # c_type, c_data = parse_header(content_type)
    # c_data["boundary"] = bytes(c_data["boundary"], "utf-8")
    # if event.get("isBase64Encoded"):
    #     body = base64.b64decode(event["body"])
    # else:
    #     body = bytes(event["body"], "utf-8")
    # body_file = BytesIO(body)
    # form_data = parse_multipart(body_file, c_data)
    # parsed_data = {}
    # for key, value in form_data.items():
    #     parsed_data[key] = value[0] if len(value) != 0 else None

    # return parsed_data
    headers = event["headers"]
    body = event["body"]
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body)
    else:
        body = bytes(body, "utf-8")
    fp = BytesIO(body)
    fs = FieldStorage(
        fp=fp,
        headers={
            "content-type": headers["Content-Type"],
            "content-length": str(fp.getbuffer().nbytes),
        },
        environ={
            "REQUEST_METHOD": "POST",
            "CONTENT_TYPE": headers["Content-Type"],
        },
        keep_blank_values=True,
    )

    #  for key in fs.keys():
    #      val = fs[key]
    #      value = val.value
    #      if not val.filename and "\r\n" in value:
    #          print("Found incorrectly parsed field")
    #          value = value[: value.index("\r\n")]
    #      form_data[key] = value
    #      # print(key, ":", fs[key].value)
    return fs


def get_new_assignment(state: State, _type: Type):
    nr_of_digits = randint(2, 5)
    content = [{"N": str(randint(1, 8))} for _ in range(nr_of_digits)]
    assignment = Assignment(state, _type, content)
    return assignment
