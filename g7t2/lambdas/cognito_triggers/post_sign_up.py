import json
import os

import boto3

from utils.utils import get_endpoint_url


def handle(event, context):
    endpoint_url = get_endpoint_url()

    # comma separated list of arns
    topic_arns_string: str = os.environ.get("topic_arns", "")
    topic_arns = topic_arns_string.split(",") if topic_arns_string else []

    sub = event["request"]["userAttributes"]["sub"]

    print(
        f"Triggered lambda for user {sub},",
        f"publishing to {topic_arns_string}",
    )

    dynamodb = boto3.client("dynamodb", endpoint_url=endpoint_url)

    print(f"Seeding db for user {sub}")
    table = os.environ["TABLE_NAME"]
    seed_data = {
        "UserId": {"S": sub},
        "Solved": {"L": []},
        "Unsolved": {"L": []},
    }
    dynamodb.put_item(TableName=table, Item=seed_data)
    print(f"Seeded data for {sub}")

    sns_client = boto3.client("sns", endpoint_url=endpoint_url)

    for arn in topic_arns:
        message = {"sub": sub, "quantity": 10}

        try:
            sns_client.publish(
                TopicArn=arn,
                Message=json.dumps(message),
            )
            print(f"Successfully published to {arn}")
        except sns_client.meta.client.exceptions.NotFoundException:
            print(f"Unable to find topic with arc {arn}")

    return {"statusCode": 200, "body": {}}
