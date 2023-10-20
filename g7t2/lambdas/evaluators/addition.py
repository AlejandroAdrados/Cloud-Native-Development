import os

import boto3
import json
from entity.assignment import State, Type, Assignment
from utils import utils


def handle(event, context):
    # get solution from user
    message = json.loads(json.loads(event["Records"][0]["body"])["Message"])
    assignment_id = message["assignment_id"]
    user_solution = int(message["solution"])
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

    fetched_assignment = None
    # get solved assignment
    for i, assignment in enumerate(unsolved_assignments):
        # found solved assignment
        if assignment["Id"] == assignment_id:
            print(f"Found assignment with id {assignment_id}")

            correct_solution = 0
            for num in assignment["Content"]:
                correct_solution += int(num)

            fetched_assignment = Assignment(
                State.INCORRECT,
                Type.ADDITION,
                utils.list_to_dynamo_list(assignment["Content"]),
            )

            if correct_solution == user_solution:
                print(f"Solution correct: {user_solution}")
                fetched_assignment.state = State.CORRECT
            else:
                print(
                    f"Solution incorrect: {user_solution},",
                    f"should be {correct_solution}",
                )

            # remove from unsolved and persist as correct/incorrect
            utils.remove_assignment(dynamodb_client, i, uid)
            utils.persist_assignment(
                dynamodb_client, table_name, fetched_assignment, uid
            )

            break

    if fetched_assignment is not None:
        return {"statusCode": 201, "body": fetched_assignment.state.value}
    else:
        message = f"Unable to find assigment with id {assignment_id}"
        print(message)
        return {
            "statusCode": 404,
            "body": json.dumps(
                {"error": f"Unable to find assigment with id {assignment_id}"}
            ),
        }
