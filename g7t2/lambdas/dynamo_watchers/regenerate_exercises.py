import boto3
import os
import json

from entity.assignment import Type
from utils.utils import get_endpoint_url


def handle(event, context):
    """
    Generate new exercises for each user and for each topic
    type where number of assignments is smaller than threshold.
    """
    print("regenerate_exercises invoked")

    EXERCISE_THRESHOLD = 5
    sns_client = boto3.client("sns", endpoint_url=get_endpoint_url())
    sns_topics = get_sns_topics()

    # get potential userids (the ones with recently solved exercise)
    potential_uids = get_userids_with_deleted_exercise(event["Records"])

    # get topics for each userid that need new exercsises
    table = get_dynamodb_table()
    for uid in potential_uids:
        topics = get_topics_with_too_less_exercises(
            uid, table, EXERCISE_THRESHOLD
        )

        for topic in topics:
            if topic in sns_topics:
                message = {"sub": uid, "quantity": 5}
                try:
                    sns_client.publish(
                        TopicArn=sns_topics[topic],
                        Message=json.dumps(message),
                    )
                    print(f"Successfully published to {topic}")
                except sns_client.meta.client.exceptions.NotFoundException:
                    print(f"Unable to find topic with arc {topic}")

    print("regenerate_exercises finished")


def count_assignment_type(assignments):
    """
    Count frequency of each assignment type.
    """
    cnt = {type_.value: 0 for type_ in Type}
    for assignment in assignments:
        type_ = assignment["Type"]
        if type_ not in cnt:
            cnt[type_] = 1
        else:
            cnt[type_] += 1
    return cnt


def get_sns_topics():
    """
    Fetches topic name from env for each assignment type and
    returns dict that maps assignment name to sns topic name.
    """
    sns_topics = {}
    for t in Type:
        topic_name = f"TOPIC_{t.value}"
        if topic_name in os.environ:
            sns_topics[t.value] = os.environ.get(topic_name)
    return sns_topics


def get_topics_with_too_less_exercises(uid, db, too_less_threshold):
    """
    Query unsolved exercsies from db for a specific uid.
    Next, check the number of unsolved exercises for each topic
    and if count it smaller than threshold add to set topics.
    """
    topics = set()
    # Query user data
    user_data = db.get_item(Key={"UserId": uid})["Item"]
    # Unsovled assignments of user
    unsolved_assignments = user_data["Unsolved"]
    # Count each type of unsovled assignments
    unsolved_type_cnt = count_assignment_type(unsolved_assignments)

    # Check if cnt of each type is greater than threshold
    for type_, cnt in unsolved_type_cnt.items():
        if cnt < too_less_threshold:
            # Add userid with topic to hashmap
            topics.add(type_)

    return topics


def get_userids_with_deleted_exercise(records):
    """
    Iterate over records in event to retrieve
    potential userids with too less exercises.
    """
    uids = set()
    for record in records:
        print(record)
        if (
            "dynamodb" in record
            and "Keys" in record["dynamodb"]
            and "UserId" in record["dynamodb"]["Keys"]
        ):
            # Get userid of record
            uid = record["dynamodb"]["Keys"]["UserId"]["S"]
            uids.add(uid)
    return uids


def get_dynamodb_table():
    """
    Returns instance of dynamodb assignment table.
    """
    endpoint_url = get_endpoint_url()
    dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
    table_name = os.environ["TABLE_NAME"]
    table = dynamodb.Table(table_name)
    return table
