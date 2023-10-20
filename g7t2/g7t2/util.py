from aws_cdk import Aws
from aws_cdk.aws_apigateway import (
    AwsIntegration,
    IntegrationOptions,
    IntegrationResponse,
    PassthroughBehavior,
)
from aws_cdk.aws_iam import Role
from aws_cdk.aws_sns import Topic


def createSNSIntegration(
    gateway_execution_role: Role, topic: Topic
) -> AwsIntegration:
    integration_options = IntegrationOptions(
        # https://github.com/aws/aws-cdk/issues/21099
        credentials_role=gateway_execution_role,  # type: ignore
        passthrough_behavior=PassthroughBehavior.NEVER,
        request_parameters={
            "integration.request.header.Content-Type": "'application/x-www-form-urlencoded'"  # noqa: E501
        },
        request_templates={
            "application/json": (
                "Action=Publish"
                f"&TopicArn=$util.urlEncode('{topic.topic_arn}')"
                "&Message=$util.urlEncode($input.body)"
            ),
        },
        integration_responses=[
            IntegrationResponse(
                status_code="200",
                response_templates={
                    "application/json": (
                        '{"status": "message added to topic"}'
                    ),
                },
                response_parameters={
                    "method.response.header.Content-Type": "application/json"
                },
            ),
            IntegrationResponse(
                status_code="400",
                selection_pattern="^\[Error\].*",  # type: ignore # noqa: W605
                response_templates={
                    "application/json": (
                        "{"
                        '"state":"error",'
                        '"message":"$util.escapeJavaScript('
                        "$input.path('$.errorMessage'))\""
                        "}"
                    ),
                },
            ),
        ],
    )
    return AwsIntegration(
        service="sns",
        integration_http_method="POST",
        path=f"{Aws.ACCOUNT_ID}/{topic.topic_name}",
        options=integration_options,
    )
