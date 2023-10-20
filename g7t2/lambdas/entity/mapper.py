# https://github.com/ap3xx/python-contributions/blob/master/aws/dynamodb_serializers.py
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer


# maps dynamodb object to python object
def dynamo_obj_to_python_obj(dynamo_obj: dict) -> dict:
    deserializer = TypeDeserializer()
    return {k: deserializer.deserialize(v) for k, v in dynamo_obj.items()}


# maps python object to dynamodb object
def python_obj_to_dynamo_obj(python_obj: dict) -> dict:
    serializer = TypeSerializer()
    return {k: serializer.serialize(v) for k, v in python_obj.items()}
