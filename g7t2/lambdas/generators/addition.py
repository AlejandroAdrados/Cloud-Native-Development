import json
import boto3
import os

from entity.assignment import State, Type
from utils import utils


def handle(event, context):
    print("addition-generator invoked")

    message = json.loads(json.loads(event["Records"][0]["body"])["Message"])
    uid = message["sub"]
    quantity = message["quantity"]
    print(f"generate {quantity} addition assignments for user {uid}")

    client = boto3.client("dynamodb", endpoint_url=utils.get_endpoint_url())
    table = os.environ["TABLE_NAME"]
    for _ in range(int(quantity)):
        assignment = utils.get_new_assignment(State.UNSOLVED, Type.ADDITION)
        utils.persist_assignment(client, table, assignment, uid)
