import boto3
import os
import utils.utils as utils


TEST_DATA = {
    "UserId": {"S": "2544b3f3-ca60-4ee4-9175-3ae772aaf624"},
    "Unsolved": {
        "L": [
            {
                "M": {
                    "Id": {"S": "ae167040-01f9-4073-adbd-395f9ea9acf4"},
                    "Type": {"S": "ADD"},
                    "Content": {"L": [{"N": "3"}, {"N": "2"}]},
                    "State": {"S": "UNSOLVED"},
                }
            },
            {
                "M": {
                    "Id": {"S": "7119950d-9d76-4488-b9c0-3c3ed0d48c43"},
                    "Type": {"S": "MULT"},
                    "Content": {"L": [{"N": "3"}, {"N": "2"}]},
                    "State": {"S": "UNSOLVED"},
                }
            },
        ]
    },
    "Solved": {
        "L": [
            {
                "M": {
                    "Id": {"S": "f748fffb-d1e0-4004-b960-a3a7d04e69eb"},
                    "Type": {"S": "ADD"},
                    "Content": {"L": [{"N": "3"}, {"N": "2"}]},
                    "State": {"S": "CORRECT"},
                }
            },
            {
                "M": {
                    "Id": {"S": "d9437c5d-9462-4b25-82a9-ee7a9b3aa898"},
                    "Type": {"S": "MULT"},
                    "Content": {"L": [{"N": "3"}, {"N": "2"}]},
                    "State": {"S": "INCORRECT"},
                }
            },
        ]
    },
}


def handle(event, context):
    # sub = utils.get_user_identifier(event)
    # TEST_DATA["UserId"]["S"] = sub
    client = boto3.client("dynamodb", endpoint_url=utils.get_endpoint_url())
    table = os.environ["TABLE_NAME"]
    value = client.put_item(TableName=table, Item=TEST_DATA)

    return {"statusCode": 201, "body": value}
