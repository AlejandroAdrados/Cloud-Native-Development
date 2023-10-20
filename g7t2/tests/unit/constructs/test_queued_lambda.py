from aws_cdk import Stack, aws_lambda as lambda_
from aws_cdk.assertions import Template
import pytest

from g7t2.g7t2.constructs.queued_lambda import QueuedLambda


@pytest.fixture
def dummy_queued_lambda_template():
    stack = Stack()
    queued_lambda = QueuedLambda(
        stack,
        "test",
        "test-topic",
        lambda_.Code.from_asset("tests/unit/utils"),
        "dummy_lambda.handle",
    )

    template = Template.from_stack(stack)
    return template, queued_lambda


def test_correct_services_are_instantiated(
    dummy_queued_lambda_template: "tuple[Template, QueuedLambda]",
):
    template, _ = dummy_queued_lambda_template

    template.resource_count_is("AWS::SNS::Topic", 1)
    template.resource_count_is("AWS::SNS::Subscription", 1)
    template.resource_count_is("AWS::SQS::Queue", 1)
    template.resource_count_is("AWS::Lambda::Function", 1)


def test_subscription_is_protocol_sqs(
    dummy_queued_lambda_template: "tuple[Template, QueuedLambda]",
):
    template, _ = dummy_queued_lambda_template
    template.has_resource_properties(
        "AWS::SNS::Subscription",
        {
            "Protocol": "sqs",
        },
    )
