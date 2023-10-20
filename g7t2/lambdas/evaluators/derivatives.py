import os

import boto3
import json
from entity.assignment import State, Type, Assignment
from utils import utils


def handle(event, context):
    # get solution from user
    message = json.loads(json.loads(event["Records"][0]["body"])["Message"])
    assignment_id = message["assignment_id"]
    user_solution = message["solution"]
    uid = message["sub"]

    # load dynamodb instance
    endpoint_url = utils.get_endpoint_url()
    dynamodb_client = boto3.client("dynamodb", endpoint_url=endpoint_url)
    dynamodb_resource = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb_resource.Table(table_name)

    # fetch assignments of user
    data: dict = table.get_item(Key={"UserId": uid})  # type: ignore
    user_data: dict = data["Item"]
    unsolved_assignments: list[dict] = user_data["Unsolved"]  # type: ignore

    # get solved assignment
    for i, assignment in enumerate(unsolved_assignments):
        # found solved assignment
        if assignment["Id"] == assignment_id:

            correct_solution = get_derivative(assignment["Content"])

            fetched_assignment = Assignment(
                State.INCORRECT,
                Type.DERIVATIVE,
                utils.list_to_dynamo_list(assignment["Content"]),
            )

            if correct_solution == user_solution:
                fetched_assignment.state = State.CORRECT

            utils.remove_assignment(dynamodb_client, i, uid)
            utils.persist_assignment(
                dynamodb_client, table_name, fetched_assignment, uid
            )

            break


def get_derivative(numbers: list):
    """
    Computes derivative for numbers.
    e.g. numbers = [3, 4, 2] represents 3x^2 + 4x + 2
         solution = [6, 4] repersents 6x + 4

    Args:
        - numbers (list): list of numbers

    Returns:
        - derivative (list): solution
    """
    if len(numbers) <= 1:
        return []

    n = len(numbers)
    numbers = numbers[:-1]  # last number can be ignored

    return [num * (n - i - 1) for i, num in enumerate(numbers)]
